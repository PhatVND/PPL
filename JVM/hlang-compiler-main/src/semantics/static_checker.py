"""
Static Semantic Checker for HLang Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral
)
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)

# Import marker classes with different names to avoid conflict  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker

class StaticChecker(ASTVisitor):
    def __init__(self, ast: Program):
        self.ast = ast
        self.global_envi = {
                "print":  ((VoidType(),  [StringType()]), 'Function', None),
                "input":  ((StringType(), []),         'Function', None),
                "int":    ((IntType(),    [StringType()]),   'Function', None),
                "float":  ((FloatType(),  [StringType()]),   'Function', None),
                "str":    ((StringType(), [IntType()]),      'Function', None),
                "len":    ((IntType(),    [ArrayType(IntType(), 0)]), 'Function', None),
            }
        self.current_function: Optional[FuncDecl] = None
        self.loop_level = 0

    def check(self):
        return self.visit_program(self.ast, [self.global_envi])

    def lookup(self, name: str, env: List[Dict[str, Tuple]], kind: str) -> Optional[Tuple]:
        for scope in env:
            if name in scope and scope[name][1] == kind:
                return scope[name]
        return None

    def lookup_any(self, name: str, env: List[Dict[str, Tuple]]) -> Optional[Tuple]:
        for scope in env:
            if name in scope:
                return scope[name]
        return None

    def check_redeclared(self, name: str, kind: str, scope: Dict[str, Tuple], env: List[Dict[str, Tuple]] = None):
        # Debug log
        print(f">>> CHECKING DECL: {name} AS {kind} IN SCOPE:", list(scope.keys()))

        # 1) Cấm redeclare nếu đã có trong cùng scope
        if name in scope:
            raise Redeclared(kind, name)

        # 2) Với Constant: không cho shadowing constant của function-body scope chỉ ở nested block sâu (len(env) > 2)
        if kind == 'Constant' and env and len(env) > 2:
            parent = env[1]  # function-body scope
            if name in parent and parent[name][1] == 'Constant':
                raise Redeclared(kind, name)

        # 2) Cấm dùng tên built-in cho mọi kind phù hợp
        if env and kind in ['Variable', 'Constant', 'Parameter']:
            builtin_funcs = {"print", "input", "int", "float", "str", "len"}
            if name in builtin_funcs:
                raise Redeclared(kind, name)
            
    def check_type_compatibility(self, expected, actual, ast, is_stmt=False):
        """
        Kiểm tra xem kiểu 'actual' có tương thích với kiểu 'expected' hay không.
        Nếu không, đưa ra TypeMismatchInStatement hoặc TypeMismatchInExpression.
        """
        print(f"[DEBUG] COMPARE: expected={expected} ({type(expected)}), actual={actual} ({type(actual)}), is_stmt={is_stmt}, ast={ast}")
        if not self.are_types_compatible(expected, actual):
            if is_stmt:
                raise TypeMismatchInStatement(ast)
            else:
                raise TypeMismatchInExpression(ast)
            
    def visit_program(self, ast: Program, env):
        # 1. Thiết lập global scope
        global_scope = self.global_envi.copy()
        env = [global_scope]
        print(">>> GLOBAL ENV INIT:", list(self.global_envi.keys()))

        # 2. Lấy danh sách tất cả các khai báo (giữ thứ tự source nếu có)
        decls = getattr(ast, "_original_order", ast.const_decls + ast.func_decls)

        # 3. Đăng ký ConstDecl và FuncDecl vào global
        for decl in decls:
            if isinstance(decl, ConstDecl):
                self.check_redeclared(decl.name, 'Constant', global_scope, env)
                typ = self.visit_expression(decl.value, env) if decl.value else None
                if decl.type_annotation:
                    if typ:
                        self.check_type_compatibility(decl.type_annotation, typ, decl, is_stmt=True)
                    typ = decl.type_annotation
                if not typ:
                    raise TypeCannotBeInferred(decl)
                global_scope[decl.name] = (typ, 'Constant', None)

            elif isinstance(decl, FuncDecl):
                self.check_redeclared(decl.name, 'Function', global_scope, env)
                param_types = [p.param_type for p in decl.params]
                global_scope[decl.name] = ((decl.return_type, param_types), 'Function', None)

        # 4. Kiểm tra có entry point main hợp lệ
        main_entry = self.lookup_any("main", env)
        if not main_entry:
            raise NoEntryPoint()
        main_info = main_entry[0]
        if not (
            isinstance(main_info, tuple)
            and isinstance(main_info[0], VoidType)
            and isinstance(main_info[1], list)
            and len(main_info[1]) == 0
        ):
            raise NoEntryPoint()

        # 5. Duyệt tất cả các FuncDecl theo đúng thứ tự xuất hiện trong source
        for func in ast.func_decls:
            self.visit_func_decl(func, env)
    
    def all_paths_return(self, stmt) -> bool:
        """
        Trả về True nếu mọi đường đi trong stmt đều kết thúc bằng ReturnStmt.
        Xử lý đệ quy cho BlockStmt, IfStmt (cần cả then và else), còn lại
        bất kỳ thứ gì khác (ReturnStmt) thì False nếu không phải Return.
        """
        # Nếu đây là 1 block, thì phải có ít nhất 1 statement và cuối cùng là return,
        # hoặc có nhiều đường đi nhưng đều return.
        if isinstance(stmt, BlockStmt):
            for s in stmt.statements:
                if self.all_paths_return(s):
                    return True
            return False

        # IfStmt: cần cả hai nhánh then và else đều trả về
        if isinstance(stmt, IfStmt):
            # 1) then branch phải return
            then_ok = self.all_paths_return(stmt.then_stmt)
            # 2) mọi elif branch cũng phải return
            elif_ok = all(self.all_paths_return(branch) 
                          for _, branch in stmt.elif_branches)
            # 3) else branch phải return
            else_ok = stmt.else_stmt and self.all_paths_return(stmt.else_stmt)
            return then_ok and elif_ok and else_ok
        
        # Nếu gặp ReturnStmt thì đường đi này chắc chắn return
        if isinstance(stmt, ReturnStmt):
            return True

        # Với các stmt khác (var decl, expr, loop, ...) không đảm bảo return
        return False

    def visit_func_decl(self, ast: FuncDecl, env):
        print(">>> ENTERING FUNC. ENV =", [list(s.keys()) for s in env])
        self.current_function = ast

        # Scope cho parameter
        param_scope = {}
        for p in ast.params:
            self.check_redeclared(p.name, 'Parameter', param_scope, env)
            param_scope[p.name] = (p.param_type, 'Parameter', None)

        new_env = [param_scope] + env


        self.visit_block_stmt(ast.body, new_env, is_func_body=True)

        if not isinstance(ast.return_type, VoidType):
            if not self.all_paths_return(ast.body):
                # “unpack” BlockStmt thành list để __str__(FuncDecl) có thể iterate
                if isinstance(ast.body, BlockStmt):
                    ast.body = ast.body.statements
                raise TypeMismatchInStatement(ast)

        self.current_function = None

    


    def visit_block_stmt(self, ast: BlockStmt, env, is_func_body=False):
        # Nếu là block ngoài cùng của function, không tạo scope mới (param_scope đã ở đầu)
        if is_func_body:
            new_env = env
        else:
            new_scope = {}
            new_env = [new_scope] + env

        print(">>> BLOCK SCOPE LAYERS =", [list(s.keys()) for s in new_env])
        for stmt in ast.statements:
            if isinstance(stmt, VarDecl):
                self.visit_var_decl(stmt, new_env)
            elif isinstance(stmt, ConstDecl):
                self.visit_const_decl(stmt, new_env)
            elif isinstance(stmt, Assignment):
                self.visit_assignment(stmt, new_env)
            elif isinstance(stmt, IfStmt):
                self.visit_if_stmt(stmt, new_env)
            elif isinstance(stmt, WhileStmt):
                self.visit_while_stmt(stmt, new_env)
            elif isinstance(stmt, ForStmt):
                self.visit_for_stmt(stmt, new_env)
            elif isinstance(stmt, ReturnStmt):
                self.visit_return_stmt(stmt, new_env)
            elif isinstance(stmt, BreakStmt):
                self.visit_break_stmt(stmt, new_env)
            elif isinstance(stmt, ContinueStmt):
                self.visit_continue_stmt(stmt, new_env)
            elif isinstance(stmt, ExprStmt):
                self.visit_expr_stmt(stmt, new_env)
            elif isinstance(stmt, BlockStmt):
                self.visit_block_stmt(stmt, new_env)
            else:
                raise Exception(f"Unknown statement type: {type(stmt)}")
                
    def visit_var_decl(self, ast: VarDecl, env):
        cur = env[0]
        self.check_redeclared(ast.name, 'Variable', cur, env)

        if isinstance(ast.value, ArrayLiteral):
            elems = ast.value.elements
            if isinstance(ast.type_annotation, ArrayType):
                # 1) Kiểm tra độ dài
                if len(elems) != ast.type_annotation.size:
                    raise TypeMismatchInStatement(ast)
                # 2) Kiểm tra kiểu từng phần tử
                expected_ty = ast.type_annotation.element_type
                for e in elems:
                    actual_ty = self.visit_expression(e, env)
                    if not self.are_types_compatible(expected_ty, actual_ty):
                        # dùng ast.value để lỗi in ra ArrayLiteral(...)
                        raise TypeMismatchInStatement(ast.value)
                rhs_type = ast.type_annotation
            else:
                # logic cũ cho literal rỗng / infer
                if len(elems) == 0:
                    raise TypeCannotBeInferred(ast)
                rhs_type = self.visit_expression(ast.value, env)
        else:
            rhs_type = self.visit_expression(ast.value, env) if ast.value else None

        if rhs_type is not None and isinstance(rhs_type, VoidType):
            raise TypeMismatchInStatement(ast)

        # Bắt lỗi pipeline trả về void trong var declaration
        # if isinstance(ast.value, BinaryOp) and ast.value.operator == '>>' \
        #    and isinstance(rhs_type, VoidType):
        #     raise TypeMismatchInStatement(ast)

        typ = ast.type_annotation
        # Nếu có ghi chú kiểu, và RHS trả về void thì lỗi
        if typ:
            if rhs_type is not None and isinstance(rhs_type, VoidType):
                raise TypeMismatchInStatement(ast)
            # rồi tiếp tục check tương thích bình thường
            self.check_type_compatibility(typ, rhs_type, ast, is_stmt=True)
        else:
            # infer: phải có RHS để infer
            if not rhs_type:
                raise TypeCannotBeInferred(ast)
            typ = rhs_type

        cur[ast.name] = (typ, 'Variable', None)

    def visit_assignment(self, ast: Assignment, env):
        rhs_type = self.visit_expression(ast.value, env)
        if isinstance(ast.lvalue, IdLValue):
            lhs_info = self.lookup_any(ast.lvalue.name, env)
            if not lhs_info:
                raise Undeclared(IdentifierMarker(), ast.lvalue.name)
            # Kiểm tra xem có đang gán lại cho hằng số không
            if lhs_info[1] == 'Constant':
                raise TypeMismatchInStatement(ast)
            lhs_type = lhs_info[0] # Lấy kiểu đã được lưu
        elif isinstance(ast.lvalue, ArrayAccessLValue):
            lhs_type = self.visit_array_access_lvalue(ast.lvalue, env)
        else:
            raise Exception(f"Unknown lvalue type: {type(ast.lvalue)}")
        self.check_type_compatibility(lhs_type, rhs_type, ast, is_stmt=True)

    def visit_identifier(self, ast: Identifier, env):
        # print(f"DEBUG: Visiting Identifier: {ast.name}") # DEBUG
        info = self.lookup_any(ast.name, env)
        if not info: 
            raise Undeclared(IdentifierMarker(), ast.name)
        # print(f"DEBUG: Identifier {ast.name} resolved to: {info}, type: {type(info)}") # DEBUG

        decl_node_or_type = info[0] # Lấy thông tin đầu tiên trong tuple
        decl_kind = info[1]
        return decl_node_or_type

    def visit_id_lvalue(self, ast: IdLValue, env):
        info = self.lookup_any(ast.name, env)
        if not info:
            raise Undeclared(IdentifierMarker(), ast.name)
        return info[0] # Trả về kiểu của lvalue

    def visit_function_call(self, ast: FunctionCall, env, is_stmt=False):
        if not isinstance(ast.function, Identifier):
            if is_stmt:
                raise TypeMismatchInStatement(ast)
            else:
                raise TypeMismatchInExpression(ast)
        
        # Tìm kiếm hàm bằng lookup_any
        func_info = self.lookup_any(ast.function.name, env)
        
        if not func_info or func_info[1] != 'Function': # Kiểm tra xem nó có phải là hàm không
            raise Undeclared(FunctionMarker(), ast.function.name)
        
        func_type_repr = func_info[0] # Lấy biểu diễn kiểu hàm (tuple)
        
        if not (isinstance(func_type_repr, tuple) and len(func_type_repr) == 2 and isinstance(func_type_repr[1], list)):
            # raise Exception(f"Invalid function type representation for {ast.function.name}: {func_type_repr}")
            raise TypeMismatchInExpression(ast)

        return_type = func_type_repr[0]
        param_types = func_type_repr[1]

        if len(ast.args) != len(param_types):
            raise TypeMismatchInStatement(ast) if is_stmt else TypeMismatchInExpression(ast)

        for i in range(len(ast.args)):
            arg_type = self.visit_expression(ast.args[i], env)
            self.check_type_compatibility(param_types[i], arg_type, ast, is_stmt) # Kiểm tra từng tham số

        return return_type

    def visit_expr_stmt(self, ast: ExprStmt, env):
        # Nếu là gọi hàm, cần kiểm tra đặc biệt để raise lỗi đúng ngữ cảnh
        if isinstance(ast.expr, FunctionCall):
            # Lấy kiểu trả về của hàm
            return_type = self.visit_function_call(ast.expr, env, is_stmt=True)
            # Nếu không phải void thì lỗi
            if not isinstance(return_type, VoidType):
                raise TypeMismatchInStatement(ast)
            return
        else:
            self.visit_expression(ast.expr, env, is_stmt=True)

    def visit_if_stmt(self, ast: IfStmt, env):
        # Kiểm tra điều kiện chính (if)
        cond_type = self.visit_expression(ast.condition, env)
        if not isinstance(cond_type, BoolType):
            raise TypeMismatchInStatement(ast)

        # Xử lý then_stmt
        if isinstance(ast.then_stmt, BlockStmt):
            self.visit_block_stmt(ast.then_stmt, env)
        else: # Xử lý các loại câu lệnh khác nếu then_stmt không phải BlockStmt
            self.visit_statement(ast.then_stmt, env)


        # Xử lý các nhánh elif
        for cond, then in ast.elif_branches:
            cond_type = self.visit_expression(cond, env)
            if not isinstance(cond_type, BoolType):
                raise TypeMismatchInStatement(ast)
            
            if isinstance(then, BlockStmt):
                self.visit_block_stmt(then, env)
            else: # Xử lý các loại câu lệnh khác
                self.visit_statement(then, env)

        # Xử lý else_stmt nếu có
        if ast.else_stmt:
            if isinstance(ast.else_stmt, BlockStmt):
                self.visit_block_stmt(ast.else_stmt, env)
            else: # Xử lý các loại câu lệnh khác
                self.visit_statement(ast.else_stmt, env)

    # Hàm trợ giúp để xử lý statement bất kể kiểu
    def visit_statement(self, stmt: ASTNode, env: List[Dict[str, Tuple]]):
        if isinstance(stmt, VarDecl):
            self.visit_var_decl(stmt, env)
        elif isinstance(stmt, ConstDecl):
            self.visit_const_decl(stmt, env)
        elif isinstance(stmt, Assignment):
            self.visit_assignment(stmt, env)
        elif isinstance(stmt, IfStmt):
            self.visit_if_stmt(stmt, env)
        elif isinstance(stmt, WhileStmt):
            self.visit_while_stmt(stmt, env)
        elif isinstance(stmt, ForStmt):
            self.visit_for_stmt(stmt, env)
        elif isinstance(stmt, ReturnStmt):
            self.visit_return_stmt(stmt, env)
        elif isinstance(stmt, BreakStmt):
            self.visit_break_stmt(stmt, env)
        elif isinstance(stmt, ContinueStmt):
            self.visit_continue_stmt(stmt, env)
        elif isinstance(stmt, ExprStmt):
            self.visit_expr_stmt(stmt, env)
        elif isinstance(stmt, BlockStmt):
            self.visit_block_stmt(stmt, env)

    def visit_while_stmt(self, ast: WhileStmt, env):
        # Kiểm tra điều kiện là biểu thức boolean
        cond_type = self.visit_expression(ast.condition, env)
        if not isinstance(cond_type, BoolType):
            raise TypeMismatchInStatement(ast)

        # Tăng loop level
        self.loop_level += 1

        # Thăm phần thân vòng lặp
        if isinstance(ast.body, BlockStmt):
            self.visit_block_stmt(ast.body, env)
        else: # Sử dụng hàm trợ giúp
            self.visit_statement(ast.body, env)

        # Giảm loop level
        self.loop_level -= 1

    def visit_for_stmt(self, ast: ForStmt, env):
        # Kiểm tra iterable phải là mảng
        iter_type = self.visit_expression(ast.iterable, env)
        if not isinstance(iter_type, ArrayType):
            raise TypeMismatchInStatement(ast)

        # Tăng loop level
        self.loop_level += 1

        # --- TẠO SCOPE RIÊNG CHO BIẾN VÒNG LẶP ---
        loop_scope = {}
        # Chỉ cấm redeclare trong chính loop_scope này (cho phép shadowing lên param_scope)
        self.check_redeclared(ast.variable, 'Variable', loop_scope, env)
        # Gán kiểu cho biến vòng lặp
        loop_scope[ast.variable] = (iter_type.element_type, 'Variable', None)
        # Đặt loop_scope lên đầu env
        new_env = [loop_scope] + env

        # Duyệt thân for (giờ đây thân for nằm dưới scope loop_scope)
        if isinstance(ast.body, BlockStmt):
            # MỞ SCOPE MỚI CHO BLOCK THÂN FOR (default is_func_body=False)
            self.visit_block_stmt(ast.body, new_env, is_func_body=True)
        else:
            self.visit_statement(ast.body, new_env)

        # Giảm loop level
        self.loop_level -= 1

    def visit_break_stmt(self, ast: BreakStmt, env):
        if self.loop_level == 0:
            raise MustInLoop(ast)

    def visit_continue_stmt(self, ast: ContinueStmt, env):
        if self.loop_level == 0:
            raise MustInLoop(ast)

    def visit_return_stmt(self, ast: ReturnStmt, env):
        print(f"[DEBUG][RETURN] ast.value={ast.value} ({type(ast.value)}) in function {self.current_function.name}")
        if not self.current_function: # Không có hàm hiện tại (có thể là lỗi cú pháp hoặc logic)
            # Tùy thuộc vào yêu cầu, có thể throw lỗi hoặc bỏ qua
            return

        expected_return_type = self.current_function.return_type

        if ast.value: # Có giá trị trả về
            actual_return_type = self.visit_expression(ast.value, env)
            if isinstance(expected_return_type, VoidType):
                raise TypeMismatchInStatement(ast) # Hàm void không được trả về giá trị
            self.check_type_compatibility(expected_return_type, actual_return_type, ast, is_stmt=True)
        else: # Không có giá trị trả về
            if not isinstance(expected_return_type, VoidType):
                raise TypeMismatchInStatement(ast) # Hàm không void phải trả về giá trị

    def visit_binary_op(self, ast: BinaryOp, env):
        op = ast.operator

        # Xử lý riêng pipeline operator '>>'
        if op == '>>':
            left_type = self.visit_expression(ast.left, env)
            # Nếu bên phải là Identifier (tên hàm)
            if isinstance(ast.right, Identifier):
                func_info = self.lookup_any(ast.right.name, env)
                if not func_info or func_info[1] != 'Function':
                    raise TypeMismatchInExpression(ast)
                func_type = func_info[0]  # Đây là tuple (return_type, param_types)
                if not (isinstance(func_type, tuple) and len(func_type) == 2 and isinstance(func_type[1], list)):
                    raise TypeMismatchInExpression(ast)
                return_type, param_types = func_type
                if len(param_types) != 1:
                    raise TypeMismatchInExpression(ast)
                if not self.are_types_compatible(param_types[0], left_type):
                    raise TypeMismatchInExpression(ast)
                return return_type
            # Nếu bên phải là FunctionCall
            elif isinstance(ast.right, FunctionCall):
                if not isinstance(ast.right.function, Identifier):
                    raise TypeMismatchInExpression(ast)
                func_info = self.lookup_any(ast.right.function.name, env)
                if not func_info or func_info[1] != 'Function':
                    raise TypeMismatchInExpression(ast)
                func_type = func_info[0]
                if not (isinstance(func_type, tuple) and len(func_type) == 2 and isinstance(func_type[1], list)):
                    raise TypeMismatchInExpression(ast)
                return_type, param_types = func_type
                args = ast.right.args
                if len(param_types) != len(args) + 1:
                    raise TypeMismatchInExpression(ast)
                if not self.are_types_compatible(param_types[0], left_type):
                    raise TypeMismatchInExpression(ast)
                for arg_expr, param_type in zip(args, param_types[1:]):
                    arg_type = self.visit_expression(arg_expr, env)
                    if not self.are_types_compatible(param_type, arg_type):
                        raise TypeMismatchInExpression(ast)
                return return_type
            else:
                # INVALID target (không phải hàm) -> lỗi trên toàn BinaryOp
                raise TypeMismatchInExpression(ast)

        # Các toán tử khác
        left = self.visit_expression(ast.left, env)
        right = self.visit_expression(ast.right, env)
        op = ast.operator

        # Kiểm tra nếu bất kỳ toán hạng nào là biểu diễn kiểu hàm (tuple)
        if (isinstance(left, tuple) and len(left) == 2) or \
           (isinstance(right, tuple) and len(right) == 2):
            raise TypeMismatchInExpression(ast)  # Không thể thực hiện phép toán với hàm

        if op in ['+', '-', '*', '/']:
            if isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType)):
                return FloatType() if FloatType in [type(left), type(right)] else IntType()
            if op == '+' and isinstance(left, StringType) and isinstance(right, StringType):
                return StringType()

        elif op == '%':
            if isinstance(left, IntType) and isinstance(right, IntType):
                return IntType()

        elif op in ['==', '!=']:
            if type(left) == type(right) and not isinstance(left, (ArrayType, VoidType)):
                return BoolType()

        elif op in ['<', '>', '<=', '>=']:
            if isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType)):
                return BoolType()

        elif op in ['&&', '||']:
            if isinstance(left, BoolType) and isinstance(right, BoolType):
                return BoolType()

        raise TypeMismatchInExpression(ast)

    def visit_unary_op(self, ast: UnaryOp, env):
        operand = self.visit_expression(ast.operand, env)
        # Kiểm tra nếu toán hạng là biểu diễn kiểu hàm (tuple)
        if isinstance(operand, tuple) and len(operand) == 2:
            raise TypeMismatchInExpression(ast) # Không thể thực hiện phép toán với hàm

        if ast.operator == '-' and isinstance(operand, (IntType, FloatType)):
            return operand
        if ast.operator == '!' and isinstance(operand, BoolType):
            return BoolType()
        raise TypeMismatchInExpression(ast)

    def visit_array_access(self, ast: ArrayAccess, env):
        # 👉 Nếu là lvalue thì gọi lại chính hàm xử lý lvalue
        if isinstance(ast.array, ArrayAccessLValue):
            arr = self.visit_array_access_lvalue(ast.array, env)
        elif isinstance(ast.array, ArrayAccess):
            arr = self.visit_array_access(ast.array, env)
        elif isinstance(ast.array, Identifier):
            arr = self.visit_identifier(ast.array, env)
        else:
            arr = self.visit_expression(ast.array, env)

        idx = self.visit_expression(ast.index, env)

        if (isinstance(arr, tuple) and len(arr) == 2) or \
        (isinstance(idx, tuple) and len(idx) == 2):
            raise TypeMismatchInExpression(ast)

        # Kiểm tra riêng biệt để chỉ rõ lỗi ở biểu thức cụ thể
        if not isinstance(arr, ArrayType):
            raise TypeMismatchInExpression(ast)

        if not isinstance(idx, IntType):
            raise TypeMismatchInExpression(ast.index)


        return arr.element_type

    def visit_array_access_lvalue(self, ast: ArrayAccessLValue, env):
        return self.visit_array_access(ast, env)

    def visit_integer_literal(self, ast, env): return IntType()
    def visit_float_literal(self, ast, env): return FloatType()
    def visit_boolean_literal(self, ast, env): return BoolType()
    def visit_string_literal(self, ast, env): return StringType()

    def visit_array_literal(self, ast, env):
        if not ast.elements:
            # Nếu mảng rỗng và không có kiểu tường minh, không thể suy luận
            # Nếu có kiểu tường minh, sẽ được xử lý ở nơi gọi
            raise TypeCannotBeInferred(ast)
            
        first_elem_type = self.visit_expression(ast.elements[0], env)
        
        # Kiểm tra nếu phần tử đầu tiên là biểu diễn kiểu hàm (tuple)
        if isinstance(first_elem_type, tuple) and len(first_elem_type) == 2:
            raise TypeMismatchInExpression(ast) # Mảng không thể chứa hàm

        for e in ast.elements[1:]:
            current_elem_type = self.visit_expression(e, env)
            # Kiểm tra nếu phần tử hiện tại là biểu diễn kiểu hàm (tuple)
            if isinstance(current_elem_type, tuple) and len(current_elem_type) == 2:
                raise TypeMismatchInExpression(ast) # Mảng không thể chứa hàm

            if not self.are_types_compatible(first_elem_type, current_elem_type):
                # TypeMismatchInStatement ở đây có thể không hoàn toàn chính xác, 
                # nhưng nó là lỗi gần nhất cho trường hợp mảng không đồng nhất
                raise TypeMismatchInExpression(ast) 
        return ArrayType(first_elem_type, len(ast.elements))
    
    def visit_int_type(self, ast, env): return ast
    def visit_float_type(self, ast, env): return ast
    def visit_bool_type(self, ast, env): return ast
    def visit_string_type(self, ast, env): return ast
    def visit_void_type(self, ast, env): return ast
    def visit_array_type(self, ast, env): return ast

    def are_types_compatible(self, expected, actual):
        if type(expected) is not type(actual):
            return False

        if isinstance(expected, ArrayType):
            return (
                expected.size == actual.size
                and self.are_types_compatible(expected.element_type, actual.element_type)
            )

        return True

        
    def visit_const_decl(self, ast: ConstDecl, env):
        cur = env[0]
        self.check_redeclared(ast.name, 'Constant', cur, env)
        
        # visit_expression sẽ trả về kiểu của giá trị khởi tạo (có thể là tuple cho hàm)
        initial_value_type = self.visit_expression(ast.value, env) if ast.value else None
        
        typ = ast.type_annotation
        
        if typ: # Nếu có kiểu chú thích tường minh
            if initial_value_type: # Nếu có giá trị khởi tạo
                self.check_type_compatibility(typ, initial_value_type, ast, is_stmt=True)
            typ = ast.type_annotation # Kiểu của hằng số là kiểu chú thích
        else: # Nếu không có kiểu chú thích, phải suy luận từ giá trị khởi tạo
            if not initial_value_type:
                raise TypeCannotBeInferred(ast)
            typ = initial_value_type # Kiểu của hằng số được suy luận
            
        cur[ast.name] = (typ, 'Constant', None) # Lưu kiểu đã suy luận/chú thích của hằng số

    def visit_param(self, ast: Param, env):
        return ast.param_type
    
    def visit_expression(self, expr, env, is_stmt=False):
        if isinstance(expr, BinaryOp):
            return self.visit_binary_op(expr, env)
        elif isinstance(expr, UnaryOp):
            return self.visit_unary_op(expr, env)
        elif isinstance(expr, FunctionCall):
            return self.visit_function_call(expr, env, is_stmt)
        elif isinstance(expr, ArrayAccess):
            return self.visit_array_access(expr, env)
        elif isinstance(expr, Identifier):
            return self.visit_identifier(expr, env)
        elif isinstance(expr, IntegerLiteral):
            return self.visit_integer_literal(expr, env)
        elif isinstance(expr, FloatLiteral):
            return self.visit_float_literal(expr, env)
        elif isinstance(expr, BooleanLiteral):
            return self.visit_boolean_literal(expr, env)
        elif isinstance(expr, StringLiteral):
            return self.visit_string_literal(expr, env)
        elif isinstance(expr, ArrayLiteral):
            return self.visit_array_literal(expr, env)
        else:
            raise Exception(f"Unknown expression type: {type(expr)}")