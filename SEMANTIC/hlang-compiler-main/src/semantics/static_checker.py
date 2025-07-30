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
            # Lưu các hàm built-in với tuple (kiểu trả về, [kiểu tham số]) để đồng nhất với cách biểu diễn hàm của visit_identifier
            "print": (FuncDecl("print", [Param("val", StringType())], VoidType(), []), 'Function', None),
            "input": (FuncDecl("input", [], StringType(), []), 'Function', None),
            "int": (FuncDecl("int", [Param("s", StringType())], IntType(), []), 'Function', None),
            "float": (FuncDecl("float", [Param  ("s", StringType())], FloatType(), []), 'Function', None),
            "str": (FuncDecl("str", [Param("x", IntType())], StringType(), []), 'Function', None),  # and others
            "len": (FuncDecl("len", [Param("arr", ArrayType(IntType(), 0))], IntType(), []), 'Function', None),
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
        print(f">>> CHECKING DECL: {name} AS {kind} IN SCOPE:", list(scope.keys()))

        if name in scope:
            raise Redeclared(kind, name)

        # ✅ CHỈ cấm nếu: khai báo biến/hằng/param trùng tên với HÀM BUILT-IN
        if env and kind in ['Variable', 'Constant', 'Parameter']:
            builtin_funcs = {"print", "input", "int", "float", "str", "len"}
            if name in builtin_funcs:
                raise Redeclared(kind, name)
            
    def check_type_compatibility(self, expected, actual, ast, is_stmt=False):
        """
        Kiểm tra xem kiểu 'actual' có tương thích với kiểu 'expected' hay không.
        Nếu không, đưa ra TypeMismatchInStatement hoặc TypeMismatchInExpression.
        """
        # print(f"🔍 check_type_compatibility: expected={expected}, actual={actual}, is_stmt={is_stmt}, ast={ast}") # DEBUG
        if not self.are_types_compatible(expected, actual):
            if is_stmt:
                raise TypeMismatchInStatement(ast)
            else:
                raise TypeMismatchInExpression(ast)
            
    def visit_program(self, ast: Program, env):
        global_scope = self.global_envi.copy()  # ✅ tạo bản sao tách biệt
        env = [global_scope]
        print(">>> GLOBAL ENV INIT:", list(self.global_envi.keys()))
        decls = getattr(ast, "_original_order", ast.const_decls + ast.func_decls)

        for decl in decls:
            if isinstance(decl, ConstDecl):
                self.check_redeclared(decl.name, 'Constant', global_scope, env)
                # Khi khởi tạo hằng số, visit_expression sẽ trả về kiểu
                typ = self.visit_expression(decl.value, env) if decl.value else None
                if decl.type_annotation:
                    if typ:
                        self.check_type_compatibility(decl.type_annotation, typ, decl, is_stmt=True)
                    typ = decl.type_annotation
                if not typ:
                    raise TypeCannotBeInferred(decl)
                global_scope[decl.name] = (typ, 'Constant', None) # Lưu kiểu của hằng số
            elif isinstance(decl, FuncDecl):
                self.check_redeclared(decl.name, 'Function', global_scope, env)
                # Lưu kiểu của hàm dưới dạng tuple (return_type, [param_types])
                param_types = [p.param_type for p in decl.params]
                global_scope[decl.name] = ((decl.return_type, param_types), 'Function', None)

        # Kiểm tra hàm main
        main = self.lookup_any("main", env) # Dùng lookup_any vì không cần biết 'kind' là gì để tìm main
        if not main:
            raise NoEntryPoint()
        
        main_info = main[0] # Lấy thông tin được lưu (có thể là kiểu hàm tuple)
        
        # main_info phải là một tuple biểu diễn kiểu hàm (VoidType, [])
        if not (isinstance(main_info, tuple) and 
                len(main_info) == 2 and 
                isinstance(main_info[0], VoidType) and 
                isinstance(main_info[1], list) and 
                len(main_info[1]) == 0):
            raise NoEntryPoint()

        # Duyệt thân các hàm
        main_func = next((f for f in ast.func_decls if f.name == "main"), None)
        if main_func:
            self.visit_func_decl(main_func, env)

        # Sau khi main đã được kiểm tra, duyệt các hàm còn lại
        for func in ast.func_decls:
            if func.name != "main":
                self.visit_func_decl(func, env)


    def visit_func_decl(self, ast: FuncDecl, env):
        print(">>> ENTERING FUNC. ENV =", [list(s.keys()) for s in env])
        self.current_function = ast

        # Scope cho parameter
        param_scope = {}
        for p in ast.params:
            self.check_redeclared(p.name, 'Parameter', param_scope, env)
            param_scope[p.name] = (p.param_type, 'Parameter', None)

        new_env = [param_scope] + env

        self.visit_block_stmt(ast.body, new_env)
        self.current_function = None

    def visit_block_stmt(self, ast: BlockStmt, env):
        if not env or not isinstance(env[0], dict):
            new_scope = {}
            new_env = [new_scope] + env  # chỉ tạo scope khi chưa có
        else: 
            new_env = env

        print(">>> BLOCK SCOPE LAYERS =", [list(s.keys()) for s in env])
        for stmt in ast.statements:
            # print("DEBUG BLOCK: ", stmt) # DEBUG
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
                # print(f"DEBUG: Encountered nested BlockStmt. Calling visit_block_stmt recursively with: {stmt}") # DEBUG
                # print(f"DEBUG: Type of nested BlockStmt: {type(stmt)}") # DEBUG
                self.visit_block_stmt(stmt, new_env)
            else:
                raise Exception(f"Unknown statement type: {type(stmt)}")
                
    def visit_var_decl(self, ast: VarDecl, env):
        cur = env[0]
        self.check_redeclared(ast.name, 'Variable', cur, env)

        rhs_type = self.visit_expression(ast.value, env) if ast.value else None
        typ = ast.type_annotation

        if typ:
            if rhs_type:
                self.check_type_compatibility(typ, rhs_type, ast, is_stmt=True)
        else:
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

        # # Nếu là hàm, trả về biểu diễn kiểu hàm (tuple)
        # if decl_kind == 'Function':
        #     # `decl_node_or_type` ở đây là tuple (return_type, param_types) đã lưu từ visit_program
        #     return decl_node_or_type 
        # # Nếu là biến, hằng, tham số, trả về kiểu của chúng
        # elif decl_kind in ['Variable', 'Constant', 'Parameter']:
        #     return decl_node_or_type # Kiểu đã được lưu trực tiếp
        # else:
        #     # Trường hợp khác nếu có, trả về chính nó
        #     return decl_node_or_type
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
            self.visit_function_call(ast.expr, env, is_stmt=True)
        else:
            self.visit_expression(ast.expr, env)

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
        else:
            raise Exception(f"Unknown statement type in visit_statement: {type(stmt)}")

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
        iter_type = self.visit_expression(ast.iterable, env)
        if not isinstance(iter_type, ArrayType):
            raise TypeMismatchInStatement(ast)

        self.loop_level += 1

        # Tạo loop scope chứa biến lặp
        loop_scope = {}
        # check_redeclared nên kiểm tra trong scope hiện tại (env[0]), không phải toàn bộ env
        self.check_redeclared(ast.variable, 'Variable', env[0], env) 
        loop_scope[ast.variable] = (iter_type.element_type, 'Variable', None)

        # Đưa vào env trước khi xử lý body
        new_env = [loop_scope] + env

        # Duyệt body
        if isinstance(ast.body, BlockStmt):
            self.visit_block_stmt(ast.body, new_env)
        else:
            self.visit_statement(ast.body, new_env)

        self.loop_level -= 1

    def visit_break_stmt(self, ast: BreakStmt, env):
        if self.loop_level == 0:
            raise MustInLoop(ast)

    def visit_continue_stmt(self, ast: ContinueStmt, env):
        if self.loop_level == 0:
            raise MustInLoop(ast)

    def visit_return_stmt(self, ast: ReturnStmt, env):
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
        left = self.visit_expression(ast.left, env)
        right = self.visit_expression(ast.right, env)
        op = ast.operator

        # Kiểm tra nếu bất kỳ toán hạng nào là biểu diễn kiểu hàm (tuple)
        if (isinstance(left, tuple) and len(left) == 2) or \
           (isinstance(right, tuple) and len(right) == 2):
           raise TypeMismatchInExpression(ast) # Không thể thực hiện phép toán với hàm

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

        if not isinstance(arr, ArrayType) or not isinstance(idx, IntType):
            raise TypeMismatchInExpression(ast)

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
                raise TypeMismatchInStatement(ast) 
        return ArrayType(first_elem_type, len(ast.elements))
    
    def visit_int_type(self, ast, env): return ast
    def visit_float_type(self, ast, env): return ast
    def visit_bool_type(self, ast, env): return ast
    def visit_string_type(self, ast, env): return ast
    def visit_void_type(self, ast, env): return ast
    def visit_array_type(self, ast, env): return ast

    def are_types_compatible(self, expected, actual):
        # return type(expected) is type(actual)
        # if isinstance(expected, FloatType) and isinstance(actual, IntType):
        #     return True  # ✅ chỉ ở cấp độ scalar
        # if type(expected) is not type(actual):
        #     return False

        # if isinstance(expected, ArrayType) and isinstance(actual, ArrayType):
        #     # ❗ Không dùng đệ quy cho int→float nữa
        #     return (
        #         expected.size == actual.size
        #         and type(expected.element_type) is type(actual.element_type)
        #     )

        # return type(expected) is type(actual)
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
    
    def visit_expression(self, expr, env):
        if isinstance(expr, BinaryOp):
            return self.visit_binary_op(expr, env)
        elif isinstance(expr, UnaryOp):
            return self.visit_unary_op(expr, env)
        elif isinstance(expr, FunctionCall):
            return self.visit_function_call(expr, env)
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