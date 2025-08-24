"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        # Tạo global_env với IO_SYMBOL_LIST và các hàm user-defined
        global_env = IO_SYMBOL_LIST[:]
        for decl in node.func_decls:
            if isinstance(decl, FuncDecl):
                param_types = [p.param_type for p in decl.params]
                return_type = decl.return_type
                ftype = FunctionType(param_types, return_type)
                global_env.append(Symbol(decl.name, ftype, CName(self.class_name)))

        # Generate code cho các hàm
        for decl in node.func_decls:
            self.visit(decl, SubBody(None, global_env))

        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )
        self.emit.emit_epilog()

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        # Xử lý như var toàn cục nếu ở <clinit>, còn trong hàm thì như local final
        # Ở codegen rút gọn này ta treat giống var_decl nhưng không cho gán lại (checker xử lý phần “const”)
        return self.visit_var_decl(VarDecl(node.name, node.type_annotation, node.value), o)
    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        frame = Frame(node.name, node.return_type)
        self.generate_method(node, SubBody(frame, o.sym))
        param_types = list(map(lambda x: x.param_type, node.params))
        return SubBody(
            None,
            [
                Symbol(
                    node.name,
                    FunctionType(param_types, node.return_type),
                    CName(self.class_name),
                )
            ]
            + o.sym,
        )

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system
    def visit_int_type(self, node: "IntType", o: Any = None): return IntType()
    def visit_float_type(self, node: "FloatType", o: Any = None): return FloatType()
    def visit_bool_type(self, node: "BoolType", o: Any = None): return BoolType()
    def visit_string_type(self, node: "StringType", o: Any = None): return StringType()
    def visit_void_type(self, node: "VoidType", o: Any = None): return VoidType()
    def visit_array_type(self, node: "ArrayType", o: Any = None): return node  # giữ nguyên

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.type_annotation,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        if node.value is not None:
            self.visit(
                Assignment(IdLValue(node.name), node.value),
                SubBody(
                    o.frame,
                    [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
                ),
            )
        return SubBody(
            o.frame,
            [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
        )

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        rc, rt = self.visit(node.value, Access(o.frame, o.sym))
        self.emit.print_out(rc)
        lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym))
        self.emit.print_out(lc)
        return o
    def ends_with_return(self, stmt):
        if isinstance(stmt, BlockStmt):
            return len(stmt.statements) > 0 and isinstance(stmt.statements[-1], ReturnStmt)
        return isinstance(stmt, ReturnStmt)
    def visit_if_stmt(self, node: "IfStmt", o: SubBody = None):
        frame = o.frame
        has_else = node.else_stmt is not None
        else_label = frame.get_new_label() if has_else else None
        end_label = frame.get_new_label()

        # Emit condition
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(
            self.emit.emit_if_false(else_label if has_else else end_label, frame)
        )

        # Emit then branch
        self.visit(node.then_stmt, o)
        then_has_return = self.ends_with_return(node.then_stmt)

        # If no return at end of then, jump to end
        if has_else and not then_has_return:
            self.emit.print_out(self.emit.emit_goto(end_label, frame))

        # Else branch
        if has_else:
            self.emit.print_out(self.emit.emit_label(else_label, frame))
            self.visit(node.else_stmt, o)
            else_has_return = self.ends_with_return(node.else_stmt)

            # Only emit end label if one of the branches does not return
            if not then_has_return or not else_has_return:
                self.emit.print_out(self.emit.emit_label(end_label, frame))
        else:
            # No else: always need end_label
            self.emit.print_out(self.emit.emit_label(end_label, frame))

        return o
    def visit_while_stmt(self, node: "WhileStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        cond_label = frame.get_new_label()
        break_label = frame.get_break_label()
        continue_label = frame.get_continue_label()

        self.emit.print_out(self.emit.emit_label(cond_label, frame))
        ccode, ctype = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(ccode)
        self.emit.print_out(self.emit.emit_if_false(break_label, frame))

        self.visit(node.body, o)
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        self.emit.print_out(self.emit.emit_goto(cond_label, frame))
        self.emit.print_out(self.emit.emit_label(break_label, frame))
        frame.exit_loop()
        return o

    def visit_for_stmt(self, node: "ForStmt", o: SubBody = None):
            # For-in loop implementation
            o.frame.enter_scope(False)
            
            from_label = o.frame.get_start_label()
            to_label = o.frame.get_end_label()
            
            # Get array and create iterator variable
            array_code, array_type = self.visit(node.iterable, Access(o.frame, o.sym))
            
            # Create index variable
            idx_var = o.frame.get_new_index()
            self.emit.print_out(self.emit.emit_var(
                idx_var, "__idx", IntType(), 
                from_label, to_label
            ))
            
            # ForStmt.variable is a string, not an object with .name
            variable_name = node.variable if isinstance(node.variable, str) else node.variable.name
            
            # Create loop variable
            loop_var = o.frame.get_new_index()
            self.emit.print_out(self.emit.emit_var(
                loop_var, variable_name, array_type.element_type,
                from_label, to_label
            ))
            
            # Store array reference
            array_var = o.frame.get_new_index()
            self.emit.print_out(self.emit.emit_var(
                array_var, "__array", array_type,
                from_label, to_label
            ))
            
            # Initialize index to 0
            self.emit.print_out(self.emit.emit_push_iconst(0, o.frame))
            self.emit.print_out(self.emit.emit_write_var("__idx", IntType(), idx_var, o.frame))
            
            # Store array reference
            self.emit.print_out(array_code)
            self.emit.print_out(self.emit.emit_write_var("__array", array_type, array_var, o.frame))
            
            # Emit the scope start label
            self.emit.print_out(self.emit.emit_label(from_label, o.frame))
            
            label_start = o.frame.get_new_label()
            label_end = o.frame.get_new_label()
            label_continue = o.frame.get_new_label()
            
            o.frame.enter_loop()
            
            # Set continue and break labels
            o.frame.con_label[-1] = label_continue
            o.frame.brk_label[-1] = label_end
            
            # Start label
            self.emit.print_out(self.emit.emit_label(label_start, o.frame))
            
            # Check if index < array length
            self.emit.print_out(self.emit.emit_read_var("__idx", IntType(), idx_var, o.frame))
            self.emit.print_out(self.emit.emit_read_var("__array", array_type, array_var, o.frame))
            self.emit.print_out(self.emit.emit_arraylength(o.frame))
            self.emit.print_out(self.emit.emit_ificmpge(label_end, o.frame))
            
            # Load current element into loop variable
            self.emit.print_out(self.emit.emit_read_var("__array", array_type, array_var, o.frame))
            self.emit.print_out(self.emit.emit_read_var("__idx", IntType(), idx_var, o.frame))
            self.emit.print_out(self.emit.emit_aload(array_type.element_type, o.frame))
            self.emit.print_out(self.emit.emit_write_var(variable_name, array_type.element_type, loop_var, o.frame))
            
            # Update environment with loop variable
            new_env = SubBody(
                o.frame,
                [Symbol(variable_name, array_type.element_type, Index(loop_var))] + o.sym
            )
            
            # Generate body
            new_env = self.visit(node.body, new_env)
            
            # Continue label (for continue statements)
            self.emit.print_out(self.emit.emit_label(label_continue, o.frame))
            
            # Increment index
            self.emit.print_out(self.emit.emit_read_var("__idx", IntType(), idx_var, o.frame))
            self.emit.print_out(self.emit.emit_push_iconst(1, o.frame))
            self.emit.print_out(self.emit.emit_add_op("+", IntType(), o.frame))
            self.emit.print_out(self.emit.emit_write_var("__idx", IntType(), idx_var, o.frame))
            
            # Jump back to start
            self.emit.print_out(self.emit.emit_goto(label_start, o.frame))
            
            # End label
            self.emit.print_out(self.emit.emit_label(label_end, o.frame))
            
            o.frame.exit_loop()
            
            # Emit the scope end label
            self.emit.print_out(self.emit.emit_label(to_label, o.frame))
            
            o.frame.exit_scope()
            
            return o


    def visit_return_stmt(self, node: "ReturnStmt", o: SubBody = None):
        frame = o.frame
        if node.value is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
            return o
        code, typ = self.visit(node.value, Access(frame, o.sym))
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(typ, frame))
        return o
    def visit_break_stmt(self, node: "BreakStmt", o: SubBody = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: SubBody = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: SubBody = None):
        # Tạo scope mới (local vars lấy chỉ số mới; label giữ nguyên)
        frame = o.frame
        frame.enter_scope(False)

        # Dùng bản sao env để shadow
        new_o = SubBody(frame, o.sym[:])

        # QUAN TRỌNG: cập nhật new_o sau mỗi visit
        for stmt in node.statements:
            ret = self.visit(stmt, new_o)
            # hầu hết các visit(...) trả về SubBody; một số có thể trả None
            if isinstance(ret, SubBody):
                new_o = ret

        frame.exit_scope()
        # Kết thúc block: env ngoài không thay đổi
        return o

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        assert sym, f"Undeclared identifier {node.name}"

        if isinstance(sym.value, Index):
            code = self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame)
        else:
            # static/global
            code = self.emit.emit_putstatic(f"{sym.value.value}/{sym.name}", sym.type, o.frame)
        return code, sym.type
    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Any = None):
        # Sẽ bổ sung sau khi xem jasmincode.py (astore/aload cụ thể)
        raise NotImplementedError("Array write not implemented yet")

    # Expressions

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        frame = o.frame
        lc, lt = self.visit(node.left, Access(frame, o.sym))
        rc, rt = self.visit(node.right, Access(frame, o.sym))
        op = node.operator

        # String concatenation
        if op == "+" and (isinstance(lt, StringType) or isinstance(rt, StringType)):
            frame.push()
            code = ""

            code += self.emit.emitNEW("java/lang/StringBuilder")
            code += self.emit.emitDUP()

            if isinstance(lt, StringType):
                code += lc
                code += self.emit.emit_invoke_special(
                    frame,
                    "java/lang/StringBuilder/<init>",
                    FunctionType([StringType()], VoidType())
                )
            else:
                code += self.emit.emit_invoke_special(
                    frame,
                    "java/lang/StringBuilder/<init>",
                    FunctionType([], VoidType())
                )
                code += lc
                code += self.emit.emit_invoke_virtual(
                    "java/lang/StringBuilder/append",
                    FunctionType([lt], ClassType("java/lang/StringBuilder")),
                    frame
                )

            code += rc
            code += self.emit.emit_invoke_virtual(
                "java/lang/StringBuilder/append",
                FunctionType([rt], ClassType("java/lang/StringBuilder")),
                frame
            )

            code += self.emit.emit_invoke_virtual(
                "java/lang/StringBuilder/toString",
                FunctionType([], StringType()),
                frame
            )
            return code, StringType()

        # int–float promotion khi cần
        code = lc + rc
        if isinstance(lt, FloatType) and isinstance(rt, IntType):
            code = lc + self.emit.emit_i2f(frame) + rc
            rt = FloatType()
        elif isinstance(lt, IntType) and isinstance(rt, FloatType):
            code = lc + rc + self.emit.emit_i2f(frame)
            lt = FloatType()

        tt = lt  # unified operand type

        if op in ["+", "-"]:
            code += self.emit.emit_addop(op, tt, frame)
            return code, tt
        if op in ["*", "/"]:
            if op == "/" and isinstance(tt, IntType):
                lc2, _ = self.visit(node.left, Access(frame, o.sym))
                rc2, _ = self.visit(node.right, Access(frame, o.sym))
                code = lc2 + self.emit.emit_i2f(frame) + rc2 + self.emit.emit_i2f(frame)
                code += self.emit.emit_mulop("/", FloatType(), frame)
                return code, FloatType()
            code += self.emit.emit_mulop(op, tt, frame)
            return code, tt
        if op == "%":
            code += self.emit.emit_mod(frame)
            return code, tt
        if op in ["==", "!=", "<", ">", "<=", ">="]:
            code += self.emit.emit_re_op(op, tt, frame)
            return code, BoolType()
        if op == "&&":
            code += self.emit.emit_andop(frame)
            return code, BoolType()
        if op == "||":
            code += self.emit.emit_orop(frame)
            return code, BoolType()

        raise NotImplementedError(f"Operator {op} not implemented for type {type(tt).__name__}")

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        frame = o.frame
        ec, et = self.visit(node.body, Access(frame, o.sym))
        if node.op == "-":
            return ec + self.emit.emit_negop(et, frame), et
        if node.op == "!":
            return ec + self.emit.emit_not(et, frame), et
        raise NotImplementedError(f"Unary {node.op} not implemented")

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name

        if function_name == "print":
            # Push System.out
            code = self.emit.emit_get_static(
                "java/lang/System/out",
                ClassType("java/io/PrintStream"),
                o.frame
            )

            # Push argument
            arg_code, arg_type = self.visit(node.args[0], Access(o.frame, o.sym))
            code += arg_code

            # Gọi println phù hợp
            println_type = FunctionType([arg_type], VoidType())
            code += self.emit.emit_invoke_virtual(
                "java/io/PrintStream/println",
                println_type,
                o.frame
            )

            return code, VoidType()

        # Mặc định: các hàm tĩnh khác
        function_symbol = next(filter(lambda x: x.name == function_name, o.sym), None)
        if function_symbol is None:
            raise Exception(f"Function {function_name} not found")

        class_name = function_symbol.value.value
        arg_codes = []
        for arg in node.args:
            ac, _ = self.visit(arg, Access(o.frame, o.sym))
            arg_codes.append(ac)

        # Lấy return type từ function_symbol
        return_type = function_symbol.type.return_type

        return (
            "".join(arg_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name,
                function_symbol.type,
                o.frame
            ),
            return_type,   # trả đúng kiểu trả về
        )



    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        frame = o.frame
        sym = o.sym

        # Sinh mã cho array_expr và index_expr
        array_code, array_type = self.visit(node.array, Access(frame, sym))
        index_code, index_type = self.visit(node.index, Access(frame, sym))

        assert isinstance(array_type, ArrayType), "Only array access supported on array type"
        assert isinstance(index_type, IntType), "Array index must be integer"

        element_type = array_type.element_type

        code = array_code + index_code
        code += self.emit.emit_array_load(element_type, frame)

        return code, element_type
    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None):
        frame = o.frame
        elems = node.elements
        n = len(elems)

        if n == 0:
            elem_type = IntType()
        else:
            _, e0_type = self.visit(elems[0], Access(frame, o.sym))
            elem_type = e0_type

        arr_type = ArrayType(elem_type, n)

        def _elem_token(t):
            if isinstance(t, IntType):    return "int"
            if isinstance(t, FloatType):  return "float"
            if isinstance(t, BoolType):   return "boolean"
            if isinstance(t, StringType): return "java/lang/String"
            raise IllegalOperandException(f"Unsupported array element type: {type(t).__name__}")

        code = ""
        code += self.emit.emit_push_iconst(n, frame)
        code += self.emit.emit_new_array(_elem_token(elem_type))  # stack: [array]

        for i, el in enumerate(elems):
            code += self.emit.emit_dup(frame)  # dup mảng để giữ trên stack
            code += self.emit.emit_push_iconst(i, frame)  # chỉ số
            el_code, el_type = self.visit(el, Access(frame, o.sym))
            if isinstance(elem_type, FloatType) and isinstance(el_type, IntType):
                el_code += self.emit.emit_i2f(frame)
            code += el_code
            code += self.emit.emit_array_store(elem_type, frame)

        return code, arr_type

    def visit_identifier(self, node: "Identifier", o: Access = None):
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        assert sym, f"Undeclared identifier {node.name}"
        # print("[DEBUG] Identifier:", node.name)
        # print("[DEBUG] Sym list:", [s.name for s in o.sym])
        if isinstance(sym.value, Index):
            code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
        else:
            code = self.emit.emit_getstatic(f"{sym.value.value}/{sym.name}", sym.type, o.frame)
        return code, sym.type

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None):
        return self.emit.emit_push_fconst(node.value, o.frame), FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None):
        val = "true" if node.value else "false"
        return self.emit.emit_push_const(val, BoolType(), o.frame), BoolType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return (
            self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame),
            StringType(),
        )