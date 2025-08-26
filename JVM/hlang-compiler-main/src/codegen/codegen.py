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
        
        print("[DEBUG] Jasmin code:\n", "".join(self.emit.buff))

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
    
        # ✅ Đặt tên biến duy nhất cho Jasmin (VD: x_1, x_2,...)
        jasmin_name = f"{node.name}_{idx}"

        # Emit .var jasmin
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                jasmin_name,  # dùng tên duy nhất
                node.type_annotation,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        # Nếu có gán giá trị
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
        if isinstance(stmt, ReturnStmt):
            return True
        if isinstance(stmt, BlockStmt):
            if not stmt.statements:
                return False
            return self.ends_with_return(stmt.statements[-1])
        if isinstance(stmt, IfStmt):
            if not stmt.then_stmt or not stmt.else_stmt:
                return False
            return self.ends_with_return(stmt.then_stmt) and self.ends_with_return(stmt.else_stmt)
        return False
    
    def visit_if_stmt(self, node: "IfStmt", o: SubBody = None):
        """
        Phát sinh mã cho IfStmt có thể gồm: if (+ nhiều elif) + else.
        Quy tắc an toàn:
        - Luôn tạo và PHÁT end_label để mọi GOTO/IF_FALSE có đích hợp lệ.
        - Mỗi nhánh (then / từng elif / else) nếu KHÔNG kết thúc bằng return,
            thì nhảy (goto) tới end_label để tránh rơi tự do vào nhãn của nhánh khác.
        - Nhãn 'next_label' (điểm rẽ sang nhánh kế tiếp) luôn được PHÁT ngay sau khi nhánh hiện tại xử lý xong.
        """
        frame = o.frame
        end_label = frame.get_new_label()

        # ===== IF (điều kiện đầu) =====
        has_following = bool(node.elif_branches) or (node.else_stmt is not None)
        next_label = frame.get_new_label() if has_following else end_label

        # điều kiện if
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        # sai -> sang nhánh kế tiếp (elif đầu hoặc else hoặc end nếu không có gì sau)
        self.emit.print_out(self.emit.emit_if_false(next_label, frame))

        # then-block
        self.visit(node.then_stmt, o)
        then_returns = self.ends_with_return(node.then_stmt)
        if not then_returns:
            # nếu then không return thì nhảy tới end
            self.emit.print_out(self.emit.emit_goto(end_label, frame))

        # rẽ sang nhánh tiếp theo (nếu có)
        if has_following:
            self.emit.print_out(self.emit.emit_label(next_label, frame))

        # ===== ELIF CHUỖI =====
        for i, (elif_cond, elif_block) in enumerate(node.elif_branches):
            is_last_elif = (i == len(node.elif_branches) - 1)
            has_after_this = (not is_last_elif) or (node.else_stmt is not None)
            next_label = frame.get_new_label() if has_after_this else end_label

            # điều kiện elif
            ec_code, _ = self.visit(elif_cond, Access(frame, o.sym))
            self.emit.print_out(ec_code)
            # sai -> sang nhánh elif kế tiếp / else / end
            self.emit.print_out(self.emit.emit_if_false(next_label, frame))

            # block elif
            self.visit(elif_block, o)
            elif_returns = self.ends_with_return(elif_block)
            if not elif_returns:
                # không return -> nhảy tới end
                self.emit.print_out(self.emit.emit_goto(end_label, frame))

            # rẽ sang nhánh tiếp theo
            if has_after_this:
                self.emit.print_out(self.emit.emit_label(next_label, frame))

        # ===== ELSE (nếu có) =====
        if node.else_stmt is not None:
            self.visit(node.else_stmt, o)
            else_returns = self.ends_with_return(node.else_stmt)
            if not else_returns:
                # không return -> nhảy tới end
                self.emit.print_out(self.emit.emit_goto(end_label, frame))

        # ===== KẾT: luôn phát end_label =====
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
        frame = o.frame

        # Tạo scope mới (local vars lấy chỉ số mới; label giữ nguyên)
        frame.enter_scope(False)

        # Lấy label đầu/cuối để khai báo phạm vi biến
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # ✅ Emit nhãn bắt đầu block (LabelX)
        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Dùng bản sao env để shadow
        new_o = SubBody(frame, o.sym[:])

        # QUAN TRỌNG: cập nhật new_o sau mỗi visit
        for stmt in node.statements:
            ret = self.visit(stmt, new_o)
            if isinstance(ret, SubBody):
                new_o = ret

        # ✅ Emit nhãn kết thúc block (LabelY)
        self.emit.print_out(self.emit.emit_label(to_label, frame))

        # Thoát khỏi scope (để đóng lại chỉ số biến, break/continue label, ...)
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
        """
        Generate code for assigning to an array element: arr[idx] = <value-on-stack>.
        Convention in our codegen: visit_assignment() đã đặt RHS lên stack trước,
        nên ở đây ta phải sắp xếp stack theo thứ tự: array, index, value rồi store.
        """
        frame = o.frame
        sym = o.sym

        # Xác định kiểu phần tử mảng
        elem_type = None
        # Trường hợp thường gặp: array là Identifier
        if isinstance(node.array, Identifier):
            arr_sym = next(filter(lambda x: x.name == node.array.name, sym), None)
            assert arr_sym and isinstance(arr_sym.type, ArrayType), "Array lvalue must be an array identifier"
            elem_type = arr_sym.type.element_type
        else:
            # Tổng quát: suy kiểu từ biểu thức truy cập mảng ở vế phải (đã có visit_array_access)
            # hoặc giả định int nếu không suy được (ít gặp trong test)
            try:
                ac_code, ac_type = self.visit(ArrayAccess(node.array, node.index), Access(frame, sym))
                # Ta không dùng ac_code ở đây vì chỉ cần kiểu
                elem_type = ac_type if isinstance(ac_type, (IntType, FloatType, BoolType, StringType)) else IntType()
            except:
                elem_type = IntType()

        # Giá trị (RHS) đang ở đỉnh stack -> cất tạm vào 1 local để dựng lại thứ tự stack
        tmp_idx = frame.get_new_index()
        code = self.emit.emit_write_var("__arr_tmp", elem_type, tmp_idx, frame)

        # Đẩy lại array và index
        arr_code, _ = self.visit(node.array, Access(frame, sym))
        idx_code, _ = self.visit(node.index, Access(frame, sym))
        code += arr_code + idx_code

        # Lấy lại value
        code += self.emit.emit_read_var("__arr_tmp", elem_type, tmp_idx, frame)

        # Store vào phần tử mảng
        code += self.emit.emit_array_store(elem_type, frame)

        return code, elem_type

    # Expressions

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        frame = o.frame
        op = node.operator

        # ---------- Helpers ----------
        def is_stringy(t):
            # Nối chuỗi nếu có String hoặc Bool ở bất kỳ bên nào
            return isinstance(t, (StringType, BoolType))

        def flatten_plus_shallow(expr):
            # Thu thập các hạng của dãy cộng ở MỨC HIỆN TẠI theo kết hợp trái:
            # ((A+B)+C)+D  → [A, B, C, D]
            terms = []
            cur = expr
            while isinstance(cur, type(node)) and getattr(cur, "operator", None) == "+":
                terms.append(cur.right)
                cur = cur.left
            terms.append(cur)
            terms.reverse()
            return terms

        def visit_expr(e):
            return self.visit(e, Access(frame, o.sym))  # (code, type)

        def unify_num_types(lt, rt):
            # Nếu một bên float → kết quả float (int được i2f)
            if isinstance(lt, FloatType) or isinstance(rt, FloatType):
                return FloatType()
            return IntType()

        # ---------- '+' ----------
        if op == "+":
            terms = flatten_plus_shallow(node)
            visited = [visit_expr(t) for t in terms]  # [(code, type), ...]
            codes, types = zip(*visited) if visited else ([], [])

            # Có stringy -> nối chuỗi toàn bộ dãy bằng StringBuilder (NHƯNG flatten nông)
            if any(is_stringy(t) for t in types):
                parts = []
                # new StringBuilder()
                parts.append(self.emit.emitNEW("java/lang/StringBuilder"))
                frame.push()
                parts.append(self.emit.emit_dup(frame))
                parts.append(self.emit.emit_invoke_special(
                    frame,
                    "java/lang/StringBuilder/<init>",
                    FunctionType([], VoidType())
                ))
                # append từng term (mỗi term tự tính xong trước)
                for c, t in zip(codes, types):
                    parts.append(c)
                    parts.append(self.emit.emit_invoke_virtual(
                        "java/lang/StringBuilder/append",
                        FunctionType([t], ClassType("java/lang/StringBuilder")),
                        frame
                    ))
                # toString
                parts.append(self.emit.emit_invoke_virtual(
                    "java/lang/StringBuilder/toString",
                    FunctionType([], StringType()),
                    frame
                ))
                return "".join(parts), StringType()

            # Không có stringy → cộng số học 2 ngôi chuẩn
            lc, lt = visit_expr(node.left)
            rc, rt = visit_expr(node.right)
            res_t = unify_num_types(lt, rt)
            parts = [lc, rc]
            if isinstance(res_t, FloatType):
                if isinstance(lt, IntType):
                    parts.insert(1, self.emit.emit_i2f(frame))
                if isinstance(rt, IntType):
                    parts.append(self.emit.emit_i2f(frame))
            parts.append(self.emit.emit_add_op("+", res_t, frame))
            return "".join(parts), res_t

        # ---------- '-', '*', '/', '%' ----------
        if op in ["-", "*", "/", "%"]:
            lc, lt = self.visit(node.left, Access(frame, o.sym))
            rc, rt = self.visit(node.right, Access(frame, o.sym))
            res_t = unify_num_types(lt, rt)
            parts = [lc, rc]
            if isinstance(res_t, FloatType):
                if isinstance(lt, IntType):
                    parts.insert(1, self.emit.emit_i2f(frame))
                if isinstance(rt, IntType):
                    parts.append(self.emit.emit_i2f(frame))
            if op == "%":
                if not isinstance(res_t, IntType):
                    raise Exception("Modulo only supported for integers")
                parts.append(self.emit.emit_mod(frame))
                return "".join(parts), IntType()
            if op == "*":
                parts.append(self.emit.emit_mul_op("*", res_t, frame))
            elif op == "/":
                parts.append(self.emit.emit_mul_op("/", res_t, frame))
            else:
                parts.append(self.emit.emit_add_op("-", res_t, frame))
            return "".join(parts), res_t

        # ---------- Quan hệ: <, <=, >, >= ----------
        if op in ["<", "<=", ">", ">="]:
            lc, lt = self.visit(node.left, Access(frame, o.sym))
            rc, rt = self.visit(node.right, Access(frame, o.sym))
            res_t = unify_num_types(lt, rt)
            parts = [lc, rc]
            if isinstance(res_t, FloatType):
                if isinstance(lt, IntType):
                    parts.insert(1, self.emit.emit_i2f(frame))
                if isinstance(rt, IntType):
                    parts.append(self.emit.emit_i2f(frame))
            parts.append(self.emit.emit_re_op(op, res_t, frame))
            return "".join(parts), BoolType()

        # ---------- Bằng/khác: ==, != (số/bool/chuỗi) ----------
        if op in ["==", "!="]:
            lc, lt = self.visit(node.left, Access(frame, o.sym))
            rc, rt = self.visit(node.right, Access(frame, o.sym))

            # String: dùng equals(Object)
            if isinstance(lt, StringType) and isinstance(rt, StringType):
                parts = []
                parts.append(lc)   # this
                parts.append(rc)   # arg
                parts.append(self.emit.emit_invoke_virtual(
                    "java/lang/String/equals",
                    FunctionType([ClassType("java/lang/Object")], BoolType()),
                    frame
                ))
                if op == "!=":
                    parts.append(self.emit.emit_not(BoolType(), frame))
                return "".join(parts), BoolType()

            # số/bool
            res_t = unify_num_types(lt, rt) if isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)) else lt
            parts = [lc, rc]
            if isinstance(res_t, FloatType):
                if isinstance(lt, IntType):
                    parts.insert(1, self.emit.emit_i2f(frame))
                if isinstance(rt, IntType):
                    parts.append(self.emit.emit_i2f(frame))
            parts.append(self.emit.emit_re_op(op, res_t if isinstance(res_t, (IntType, FloatType)) else IntType(), frame))
            return "".join(parts), BoolType()

        # ---------- Logic: and / or (&& / ||) short-circuit ----------
        if op in ["and", "&&"]:
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            code = []
            lc, _ = self.visit(node.left, Access(frame, o.sym))
            code.append(lc)
            code.append(self.emit.emit_if_false(false_label, frame))
            rc, _ = self.visit(node.right, Access(frame, o.sym))
            code.append(rc)
            code.append(self.emit.emit_if_false(false_label, frame))
            code.append(self.emit.emit_push_const("true", BoolType(), frame))
            code.append(self.emit.emit_goto(end_label, frame))
            code.append(self.emit.emit_label(false_label, frame))
            code.append(self.emit.emit_push_const("false", BoolType(), frame))
            code.append(self.emit.emit_label(end_label, frame))
            return "".join(code), BoolType()

        if op in ["or", "||"]:
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            code = []
            lc, _ = self.visit(node.left, Access(frame, o.sym))
            code.append(lc)
            code.append(self.emit.emit_if_true(true_label, frame))
            rc, _ = self.visit(node.right, Access(frame, o.sym))
            code.append(rc)
            code.append(self.emit.emit_if_true(true_label, frame))
            code.append(self.emit.emit_push_const("false", BoolType(), frame))
            code.append(self.emit.emit_goto(end_label, frame))
            code.append(self.emit.emit_label(true_label, frame))
            code.append(self.emit.emit_push_const("true", BoolType(), frame))
            code.append(self.emit.emit_label(end_label, frame))
            return "".join(code), BoolType()

        # ---------- Fallback ----------
        lc, lt = self.visit(node.left, Access(frame, o.sym))
        rc, rt = self.visit(node.right, Access(frame, o.sym))
        raise Exception(f"Illegal Operand: Operator {op} not implemented for types {type(lt).__name__}, {type(rt).__name__}")








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
    
    