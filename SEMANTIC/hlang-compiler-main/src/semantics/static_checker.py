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
            "print": (FuncDecl("print", [Param("val", StringType())], VoidType(), BlockStmt([])), 'Function', None),
            "readInt": (FuncDecl("readInt", [], IntType(), BlockStmt([])), 'Function', None),
            "readFloat": (FuncDecl("readFloat", [], FloatType(), BlockStmt([])), 'Function', None),
            "readString": (FuncDecl("readString", [], StringType(), BlockStmt([])), 'Function', None),
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

    def check_redeclared(self, name: str, kind: str, scope: Dict[str, Tuple]):
        if name in scope:
            raise Redeclared(kind, name)
            
    def visit_program(self, ast: Program, env):
        global_scope = env[0]

        for const in ast.const_decls:
            self.check_redeclared(const.name, 'Constant', global_scope)
            const_type = self.visit_expression(const.value, env) if const.value else None
            if const.const_type:
                if const_type:
                    self.check_type_compatibility(const.const_type, const_type, const)
                const_type = const.const_type
            if not const_type:
                raise TypeCannotBeInferred(const)
            global_scope[const.name] = (const_type, 'Constant', const.value)

        for func in ast.func_decls:
            self.check_redeclared(func.name, 'Function', global_scope)
            global_scope[func.name] = (func, 'Function', None)

        main = self.lookup("main", env, 'Function')
        if not main:
            raise NoEntryPoint()
        main_decl = main[0]
        if not isinstance(main_decl, FuncDecl) or len(main_decl.params) != 0 or not isinstance(main_decl.return_type, VoidType):
            raise NoEntryPoint()

        for func in ast.func_decls:
            self.visit_func_decl(func, env)
    def visit_fun_decl(self, ast: FuncDecl, env):
        self.current_function = ast
        param_scope = {}
        for p in ast.params:
            self.check_redeclared(p.name, 'Parameter', param_scope)
            param_scope[p.name] = (p.param_type, 'Parameter', None)
        self.visit(ast.body, [param_scope] + env)
        self.current_function = None

    def visit_block_stmt(self, ast: BlockStmt, env):
        new_scope = [{}]
        for stmt in ast.statements:
            if isinstance(stmt, VarDecl):
                self.visit_var_decl(stmt, new_scope + env)
            elif isinstance(stmt, ConstDecl):
                self.visit_const_decl(stmt, new_scope + env)
            elif isinstance(stmt, Assignment):
                self.visit_assignment(stmt, new_scope + env)
            elif isinstance(stmt, IfStmt):
                self.visit_if_stmt(stmt, new_scope + env)
            elif isinstance(stmt, WhileStmt):
                self.visit_while_stmt(stmt, new_scope + env)
            elif isinstance(stmt, ForStmt):
                self.visit_for_stmt(stmt, new_scope + env)
            elif isinstance(stmt, ReturnStmt):
                self.visit_return_stmt(stmt, new_scope + env)
            elif isinstance(stmt, BreakStmt):
                self.visit_break_stmt(stmt, new_scope + env)
            elif isinstance(stmt, ContinueStmt):
                self.visit_continue_stmt(stmt, new_scope + env)
            elif isinstance(stmt, ExprStmt):
                self.visit_expr_stmt(stmt, new_scope + env)
            elif isinstance(stmt, BlockStmt):
                self.visit_block_stmt(stmt, new_scope + env)
            else:
                raise Exception(f"Unknown statement type: {type(stmt)}")
    def visit_var_decl(self, ast: VarDecl, env):
        cur = env[0]
        self.check_redeclared(ast.name, 'Variable', cur)
        rhs_type = self.visit(ast.expr, env) if ast.expr else None
        typ = ast.var_type
        if typ:
            if rhs_type:
                self.check_type_compatibility(typ, rhs_type, ast)
        else:
            if not rhs_type:
                raise TypeCannotBeInferred(ast)
            typ = rhs_type
        cur[ast.name] = (typ, 'Variable', None)

    def visit_assignment(self, ast: Assignment, env):
        rhs_type = self.visit(ast.expr, env)
        lhs_type = self.visit(ast.lvalue, env)
        if isinstance(ast.lvalue, IdLValue):
            if self.lookup(ast.lvalue.name, env, 'Constant'):
                raise TypeMismatchInStatement(ast)
        self.check_type_compatibility(lhs_type, rhs_type, ast)

    def visit_identifier(self, ast: Identifier, env):
        info = self.lookup_any(ast.name, env)
        if not info or info[1] == 'Function':
            raise Undeclared(IdentifierMarker(), ast.name)
        return info[0]

    def visit_id_lvalue(self, ast: IdLValue, env):
        info = self.lookup_any(ast.name, env)
        if not info:
            raise Undeclared(IdentifierMarker(), ast.name)
        return info[0]

    def visit_function_call(self, ast: FunctionCall, env):
        if not isinstance(ast.function, Identifier):
            raise TypeMismatchInExpression(ast)
        info = self.lookup(ast.function.name, env, 'Function')
        if not info:
            raise Undeclared(FunctionMarker(), ast.function.name)
        decl = info[0]
        if len(ast.args) != len(decl.params):
            raise TypeMismatchInExpression(ast)
        for i in range(len(ast.args)):
            arg_type = self.visit(ast.args[i], env)
            param_type = decl.params[i].param_type
            self.check_type_compatibility(param_type, arg_type, ast)
        return decl.return_type


    def visit_expr_stmt(self, ast: ExprStmt, env):
        self.visit(ast.expr, env)

    def visit_if_stmt(self, ast: IfStmt, env):
        cond_type = self.visit(ast.cond, env)
        if not isinstance(cond_type, BoolType):
            raise TypeMismatchInStatement(ast)
        self.visit(ast.then_stmt, env)
        for cond, then in ast.elif_branches:
            if not isinstance(self.visit(cond, env), BoolType):
                raise TypeMismatchInStatement(ast)
            self.visit(then, env)
        if ast.else_stmt:
            self.visit(ast.else_stmt, env)

    def visit_while_stmt(self, ast: WhileStmt, env):
        if not isinstance(self.visit(ast.cond, env), BoolType):
            raise TypeMismatchInStatement(ast)
        self.loop_level += 1
        self.visit(ast.body, env)
        self.loop_level -= 1

    def visit_for_stmt(self, ast: ForStmt, env):
        iter_type = self.visit(ast.iterable, env)
        if not isinstance(iter_type, ArrayType):
            raise TypeMismatchInStatement(ast)
        self.loop_level += 1
        new_scope = {ast.var: (iter_type.element_type, 'Variable', None)}
        self.visit(ast.body, [new_scope] + env)
        self.loop_level -= 1

    def visit_break_stmt(self, ast: BreakStmt, env):
        if self.loop_level == 0:
            raise MustInLoop(ast)

    def visit_continue_stmt(self, ast: ContinueStmt, env):
        if self.loop_level == 0:
            raise MustInLoop(ast)

    def visit_return_stmt(self, ast: ReturnStmt, env):
        if not self.current_function:
            return
        expected = self.current_function.return_type
        if ast.expr:
            actual = self.visit(ast.expr, env)
            if isinstance(expected, VoidType):
                raise TypeMismatchInStatement(ast)
            self.check_type_compatibility(expected, actual, ast)
        else:
            if not isinstance(expected, VoidType):
                raise TypeMismatchInStatement(ast)

    def visit_binary_op(self, ast: BinaryOp, env):
        left = self.visit(ast.left, env)
        right = self.visit(ast.right, env)
        op = ast.op
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
        operand = self.visit(ast.operand, env)
        if ast.op == '-' and isinstance(operand, (IntType, FloatType)):
            return operand
        if ast.op == '!' and isinstance(operand, BoolType):
            return BoolType()
        raise TypeMismatchInExpression(ast)

    def visit_array_access(self, ast: ArrayAccess, env):
        arr = self.visit(ast.array, env)
        idx = self.visit(ast.index, env)
        if not isinstance(arr, ArrayType) or not isinstance(idx, IntType):
            raise TypeMismatchInExpression(ast)
        return arr.element_type

    def visit_array_access_lvalue(self, ast: ArrayAccessLValue, env):
        return self.visitArrayAccess(ast, env)

    def visit_integer_literal(self, ast, env): return IntType()
    def visit_float_literal(self, ast, env): return FloatType()
    def visit_boolean_literal(self, ast, env): return BoolType()
    def visit_string_literal(self, ast, env): return StringType()

    def visit_array_literal(self, ast, env):
        if not ast.elements:
            raise TypeCannotBeInferred(ast)
        first = self.visit(ast.elements[0], env)
        for e in ast.elements[1:]:
            if not self.are_types_compatible(first, self.visit(e, env)):
                raise TypeMismatchInStatement(ast)
        return ArrayType(first, len(ast.elements))

    def visit_int_type(self, ast, env): return ast
    def visit_float_type(self, ast, env): return ast
    def visit_bool_type(self, ast, env): return ast
    def visit_string_type(self, ast, env): return ast
    def visit_void_type(self, ast, env): return ast
    def visit_array_type(self, ast, env): return ast

    def are_types_compatible(self, expected, actual):
        if isinstance(expected, FloatType) and isinstance(actual, IntType):
            return True
        if isinstance(expected, ArrayType) and isinstance(actual, ArrayType):
            return expected.size == actual.size and \
                   type(expected.element_type) is type(actual.element_type)
        return type(expected) is type(actual)

    def check_type_compatibility(self, expected, actual, node):
        if not self.are_types_compatible(expected, actual):
            if isinstance(node, (Assignment, ReturnStmt, IfStmt, WhileStmt, ForStmt)):
                raise TypeMismatchInStatement(node)
            raise TypeMismatchInExpression(node)
    def visit_const_decl(self, ast: ConstDecl, env):
        cur = env[0]
        self.check_redeclared(ast.name, 'Constant', cur)
        const_type = self.visit_expression(ast.value, env) if ast.value else None
        if ast.const_type:
            if const_type:
                self.check_type_compatibility(ast.const_type, const_type, ast)
            const_type = ast.const_type
        if not const_type:
            raise TypeCannotBeInferred(ast)
        cur[ast.name] = (const_type, 'Constant', ast.value)
    def visit_func_decl(self, ast: FuncDecl, env):
        self.current_function = ast
        param_scope = {}
        for p in ast.params:
            self.check_redeclared(p.name, 'Parameter', param_scope)
            param_scope[p.name] = (p.param_type, 'Parameter', None)
        self.visit_block_stmt(ast.body, [param_scope] + env)  # ✅ đã sửa
        self.current_function = None
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