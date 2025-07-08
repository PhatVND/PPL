"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *


class ASTGeneration(HLangVisitor):
    # ============================================================================
    # Program and Top-level Declarations
    # ============================================================================

    # program: declared_statement_list EOF;
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        declarations = self.visit(ctx.declared_statement_list())
        
        const_decls = [decl for decl in declarations if isinstance(decl, ConstDecl)]
        func_decls = [decl for decl in declarations if isinstance(decl, FuncDecl)]
        
        return Program(const_decls, func_decls)

    # declared_statement_list: (declared_statement) declared_statement_list | (declared_statement);
    def visitDeclared_statement_list(self, ctx: HLangParser.Declared_statement_listContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.declared_statement())]
        return [self.visit(ctx.declared_statement())] + self.visit(ctx.declared_statement_list())

    # declared_statement: constants_declared | function_declared;
    def visitDeclared_statement(self, ctx: HLangParser.Declared_statementContext):
        return self.visit(ctx.getChild(0))
          # constants_declared: CONST ID const_type_opt ASSIGN expression SEMICOLON;
    def visitConstants_declared(self, ctx: HLangParser.Constants_declaredContext):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.const_type_opt()) if ctx.const_type_opt() else None
        value = self.visit(ctx.expression())
        return ConstDecl(name, type_annotation, value)

    # const_type_opt: COLON mytype | ;
    def visitConst_type_opt(self, ctx: HLangParser.Const_type_optContext):
        return self.visit(ctx.mytype()) if ctx.mytype() else None

    # function_declared: FUNC ID ... parameter_list arrow_mytype_opt function_body_container ...;
    def visitFunction_declared(self, ctx: HLangParser.Function_declaredContext):
        name = ctx.ID().getText()
        params = self.visit(ctx.parameter_list())
        return_type = self.visit(ctx.arrow_mytype_opt())
        body = self.visit(ctx.function_body_container())
        
        # Function body returns a BlockStmt, which contains a list of statements
        return FuncDecl(name, params, return_type, body.statements)

    # parameter_list: LPAREN parameter_list_opt RPAREN;
    def visitParameter_list(self, ctx: HLangParser.Parameter_listContext):
        return self.visit(ctx.parameter_list_opt()) if ctx.parameter_list_opt() else []

    # parameter_list_opt: parameter parameter_list_prime | ;
    def visitParameter_list_opt(self, ctx: HLangParser.Parameter_list_optContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.parameter())] + self.visit(ctx.parameter_list_prime())

    # parameter_list_prime: COMMA parameter parameter_list_prime | ;
    def visitParameter_list_prime(self, ctx: HLangParser.Parameter_list_primeContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.parameter())] + self.visit(ctx.parameter_list_prime())

    # parameter: ID COLON mytype;
    def visitParameter(self, ctx: HLangParser.ParameterContext):
        name = ctx.ID().getText()
        param_type = self.visit(ctx.mytype())
        return Param(name, param_type)
        
    # arrow_mytype_opt: ARROW mytype | ;
    def visitArrow_mytype_opt(self, ctx: HLangParser.Arrow_mytype_optContext):
        return self.visit(ctx.mytype()) if ctx.mytype() else VoidType()

    # ============================================================================
    # Type System
    # ============================================================================

    # mytype: ... primitive_type | array_type ...
    def visitMytype(self, ctx: HLangParser.MytypeContext):
        # This grammar is complex and allows function types, etc.
        # For this version, we will focus on primitive and array types.
        if ctx.primitive_type():
            return self.visit(ctx.primitive_type())
        if ctx.array_type():
            return self.visit(ctx.array_type())
        if ctx.ID():
             # HLang spec doesn't define user types, but grammar allows it.
             # Treating it as a placeholder/error or a future feature.
             # For now, we'll represent it by name.
            return Identifier(ctx.ID().getText()) 
        # Handle parenthesized types
        if ctx.LPAREN():
            return self.visit(ctx.mytype(0))
        # Handle function types (omitted for brevity, as not in nodes.py)
        return None # Placeholder for more complex types

    # primitive_type: INT | FLOAT | BOOL | STRING | VOID;
    def visitPrimitive_type(self, ctx: HLangParser.Primitive_typeContext):
        if ctx.INT(): return IntType()
        if ctx.FLOAT(): return FloatType()
        if ctx.BOOL(): return BoolType()
        if ctx.STRING(): return StringType()
        if ctx.VOID(): return VoidType()

    # array_type: LBRACK mytype SEMICOLON INTEGER_LIT RBRACK ... ;
    def visitArray_type(self, ctx: HLangParser.Array_typeContext):
        # Simplified for the main HLang array syntax: [type; size]
        if ctx.SEMICOLON():
            element_type = self.visit(ctx.mytype())
            size = int(ctx.INTEGER_LIT().getText())
            return ArrayType(element_type, size)
        # Other array forms in grammar are not in HLang spec, omitted.
        return None

    # ============================================================================
    # Statements
    # ============================================================================

    # list_statement: list_statement_prime | ;
    def visitList_statement(self, ctx: HLangParser.List_statementContext):
        return self.visit(ctx.list_statement_prime()) if ctx.list_statement_prime() else []

    # list_statement_prime: statement list_statement_prime | statement;
    def visitList_statement_prime(self, ctx: HLangParser.List_statement_primeContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.statement())]
        return [self.visit(ctx.statement())] + self.visit(ctx.list_statement_prime())

    # statement: ...
    def visitStatement(self, ctx: HLangParser.StatementContext):
        return self.visit(ctx.getChild(0))

    # variables_declared: LET ID (COLON mytype (ASSIGN expression)? | ASSIGN expression) SEMICOLON;
    def visitVariables_declared(self, ctx: HLangParser.Variables_declaredContext):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.mytype()) if ctx.mytype() else None
        value = self.visit(ctx.expression()) if ctx.expression() else None
        print("DEBUG VarDecl value:", value, type(value))
        # Nếu value là list → fix tại đây luôn:
        if isinstance(value, list):
            value = value[0] if value else None
        return VarDecl(name, type_annotation, value)

    # assignment_statement: lhs_assignment_statement ASSIGN expression SEMICOLON;
    def visitAssignment_statement(self, ctx: HLangParser.Assignment_statementContext):
        lvalue = self.visit(ctx.lhs_assignment_statement())
        value = self.visit(ctx.expression())
        return Assignment(lvalue, value)

    # lhs_assignment_statement: ID | lhs_assignment_statement LBRACK expression RBRACK;
    # def visitLhs_assignment_statement(self, ctx: HLangParser.Lhs_assignment_statementContext):
    #     if ctx.getChildCount() == 1:
    #         return IdLValue(ctx.ID().getText())
        
    #     array = self.visit(ctx.lhs_assignment_statement())
    #     # The LValue AST nodes expect expressions, not LValues, for the array part.
    #     # This requires a conversion or a shared representation. We'll build it recursively.
    #     # This is a tricky part where parser grammar and AST structure might mismatch.
    #     # A simple solution is to rebuild the expression from the LValue.
    #     # Let's assume a simpler conversion for now.
    #     if isinstance(array, IdLValue):
    #         array_expr = Identifier(array.name)
    #     elif isinstance(array, ArrayAccessLValue):
    #         # This reconstructs the expression part of the LValue
    #         def lvalue_to_expr(lval):
    #             if isinstance(lval, IdLValue):
    #                 return Identifier(lval.name)
    #             elif isinstance(lval, ArrayAccessLValue):
    #                 return ArrayAccess(lvalue_to_expr(lval.array), lval.index)
    #         array_expr = lvalue_to_expr(array)
            
    #     index = self.visit(ctx.expression())
    #     return ArrayAccessLValue(array_expr, index)

    # 1) Thu thập tất cả các biểu thức trong chuỗi [expr][expr]…
    def visitLhs_assignment_statement_prime(self, ctx: HLangParser.Lhs_assignment_statement_primeContext):
        indices = []
        current = ctx
        # Lặp cho đến khi không còn prime nối tiếp
        while current is not None:
            indices.append(self.visit(current.expression()))
            current = current.lhs_assignment_statement_prime()
        return indices

    # 2) Xây dựng l-value cho assignment: phải là Identifier (Expr), không phải IdLValue
    def visitLhs_assignment_statement(self, ctx: HLangParser.Lhs_assignment_statementContext):
        # Nếu không có '[...]', đây là ID đơn thuần, dùng IdLValue
        prime = ctx.lhs_assignment_statement_prime()
        if prime is None:
            return IdLValue(ctx.ID().getText())

        # Ngược lại, là array-access: khởi tạo base Expr từ Identifier
        base_expr = Identifier(ctx.ID().getText())
        # Lấy list các index và lần lượt bọc thành ArrayAccessLValue
        for idx in self.visit(prime):
            base_expr = ArrayAccessLValue(base_expr, idx)
        return base_expr

    # if_statement: IF (LPAREN expression RPAREN) (function_body_container) else_if_clause_opt else_clause_opt;
    def visitIf_statement(self, ctx: HLangParser.If_statementContext):
        condition = self.visit(ctx.expression())
        then_stmt = self.visit(ctx.function_body_container())
        elif_branches = self.visit(ctx.else_if_clause_opt()) if ctx.else_if_clause_opt() else []
        else_stmt = self.visit(ctx.else_clause_opt()) if ctx.else_clause_opt() else None
        return IfStmt(condition, then_stmt, elif_branches, else_stmt)

    # else_if_clause_opt: else_if_clause_list | ;
    def visitElse_if_clause_opt(self, ctx: HLangParser.Else_if_clause_optContext):
        return self.visit(ctx.getChild(0)) if ctx.getChildCount() > 0 else []

    # else_if_clause_list: (else_if_clause_content) else_if_clause_list | (else_if_clause_content);
    def visitElse_if_clause_list(self, ctx: HLangParser.Else_if_clause_listContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.else_if_clause_content())]
        return [self.visit(ctx.else_if_clause_content())] + self.visit(ctx.else_if_clause_list())
        
    # else_if_clause_content: ELSE IF (LPAREN expression RPAREN) (function_body_container);
    def visitElse_if_clause_content(self, ctx: HLangParser.Else_if_clause_contentContext):
        condition = self.visit(ctx.expression())
        block = self.visit(ctx.function_body_container())
        return (condition, block)

    # else_clause_opt: else_clause | ;
    def visitElse_clause_opt(self, ctx: HLangParser.Else_clause_optContext):
        return self.visit(ctx.getChild(0)) if ctx.getChildCount() > 0 else None

    # else_clause: ELSE function_body_container;
    def visitElse_clause(self, ctx: HLangParser.Else_clauseContext):
        return self.visit(ctx.function_body_container())

    # while_statement: WHILE LPAREN expression RPAREN function_body_container;
    def visitWhile_statement(self, ctx: HLangParser.While_statementContext):
        condition = self.visit(ctx.expression())
        body = self.visit(ctx.function_body_container())
        return WhileStmt(condition, body)

    # for_statement: for_in_loop;
    def visitFor_statement(self, ctx: HLangParser.For_statementContext):
        return self.visit(ctx.for_in_loop())

    # for_in_loop: FOR LPAREN ID IN expression RPAREN function_body_container;
    def visitFor_in_loop(self, ctx: HLangParser.For_in_loopContext):
        variable = ctx.ID().getText()
        iterable = self.visit(ctx.expression())
        body = self.visit(ctx.function_body_container())
        return ForStmt(variable, iterable, body)
        
    # return_statement: RETURN return_statement_opt SEMICOLON;
    def visitReturn_statement(self, ctx: HLangParser.Return_statementContext):
        # print(">>> visitReturn_statement")
        opt_ctx = ctx.return_statement_opt()
        value = self.visit(opt_ctx) if opt_ctx else None
        # print(">>> Return value from return_statement_opt:", value)
        return ReturnStmt(value)

        
    # return_statement_opt: expression | ;
    def visitReturn_statement_opt(self, ctx: HLangParser.Return_statement_optContext):
        expr_ctx = ctx.expression()

        # Nếu không có expression
        if expr_ctx is None:
            return None

        # Nếu có expression nhưng là node rỗng (ví dụ: return;)
        if expr_ctx.getText().strip() == "":
            return None

        return self.visit(expr_ctx)

    # break_statement: BREAK SEMICOLON;
    def visitBreak_statement(self, ctx: HLangParser.Break_statementContext):
        return BreakStmt()

    # continue_statement: CONTINUE SEMICOLON;
    def visitContinue_statement(self, ctx: HLangParser.Continue_statementContext):
        return ContinueStmt()

    # call_statement: (function_call | ...) SEMICOLON;
    def visitCall_statement(self, ctx: HLangParser.Call_statementContext):
        # A call used as a statement is an expression statement
        expr = self.visit(ctx.getChild(0))
        return ExprStmt(expr)

    # block_statement: function_body_container;
    def visitBlock_statement(self, ctx: HLangParser.Block_statementContext):
        return self.visit(ctx.function_body_container())

    # function_body_container: LBRACE list_statement RBRACE;
    def visitFunction_body_container(self, ctx: HLangParser.Function_body_containerContext):
        statements = self.visit(ctx.list_statement())
        return BlockStmt(statements)

    # ============================================================================
    # Expressions
    # ============================================================================

    # list_expression: list_expression_prime | ;
    def visitList_expression(self, ctx: HLangParser.List_expressionContext):
        return self.visit(ctx.list_expression_prime()) if ctx.list_expression_prime() else []

    # list_expression_prime: expression COMMA list_expression_prime | expression;
    def visitList_expression_prime(self, ctx: HLangParser.List_expression_primeContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.expression())]
        return [self.visit(ctx.expression())] + self.visit(ctx.list_expression_prime())

    # expression: expression (PIPELINE | OR) expression1 | expression1;
    def visitExpression(self, ctx: HLangParser.ExpressionContext):
        if ctx.getChildCount() == 3:
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.getChild(0))  # thay vì ctx.expression()
            right = self.visit(ctx.getChild(2))  # thay vì ctx.expression1()
            return BinaryOp(left, op, right)
        return self.visit(ctx.getChild(0))  # ctx.expression1()

    # expression1: expression1 AND expression2 | expression2;
    def visitExpression1(self, ctx: HLangParser.Expression1Context):
        if ctx.getChildCount() == 3:
            op = ctx.AND().getText()
            left = self.visit(ctx.expression1())
            right = self.visit(ctx.expression2())
            return BinaryOp(left, op, right)
        return self.visit(ctx.expression2())

    # expression2: expression2 (EQUAL | NOT_EQUAL | ...) expression3 | expression3;
    def visitExpression2(self, ctx: HLangParser.Expression2Context):
        if ctx.getChildCount() == 3:
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression2())
            right = self.visit(ctx.expression3())
            return BinaryOp(left, op, right)
        return self.visit(ctx.expression3())

    # expression3: expression3 (ADD | SUB) expression4 | expression4;
    def visitExpression3(self, ctx: HLangParser.Expression3Context):
        if ctx.getChildCount() == 3:
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression3())
            right = self.visit(ctx.expression4())
            return BinaryOp(left, op, right)
        return self.visit(ctx.expression4())

    # expression4: expression4 (MUL | DIV | MOD) expression5 | expression5;
    def visitExpression4(self, ctx: HLangParser.Expression4Context):
        if ctx.getChildCount() == 3:
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression4())
            right = self.visit(ctx.expression5())
            return BinaryOp(left, op, right)
        return self.visit(ctx.expression5())

    # expression5: (NOT | SUB | ADD) expression5 | expression6;
    def visitExpression5(self, ctx: HLangParser.Expression5Context):
        if ctx.getChildCount() == 2:
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.expression5())
            # INCREMENT removed from here as ++x is not in HLang spec, only x++ as a statement.
            return UnaryOp(op, operand)
        return self.visit(ctx.expression6())

    # expression6: operands like literals, identifiers, calls, array access
    def visitExpression6(self, ctx: HLangParser.Expression6Context):
        if ctx.LBRACK(): # Array Access
            array = self.visit(ctx.expression6())
            index = self.visit(ctx.expression())
            return ArrayAccess(array, index)
            
        if ctx.function_call(): # Function Call
            return self.visit(ctx.function_call())
            
        if ctx.ID() and not ctx.LPAREN(): # Identifier
            return Identifier(ctx.ID().getText())
            
        if ctx.literal(): # Literal
            return self.visit(ctx.literal())

        if ctx.expression7(): # Parenthesized expression
            return self.visit(ctx.expression7())
        
        # Other grammar rules like builtin_func, anonymous_function are not directly in nodes.py
        # and are handled as generic FunctionCall/Identifier for now.
        return self.visit(ctx.getChild(0))

    # expression7: LPAREN expression RPAREN;
    def visitExpression7(self, ctx: HLangParser.Expression7Context):
        return self.visit(ctx.expression())

    # function_call: ID LPAREN list_expression RPAREN;
    def visitFunction_call(self, ctx: HLangParser.Function_callContext):
        # The 'function' part of a FunctionCall node is an expression.
        # Here, it's an identifier.
        function_expr = Identifier(ctx.ID().getText())
        args = self.visit(ctx.list_expression())
        return FunctionCall(function_expr, args)

    # ============================================================================
    # Literals
    # ============================================================================

    # literal: literal_primitive | array_literal;
    def visitLiteral(self, ctx: HLangParser.LiteralContext):
        return self.visit(ctx.getChild(0))

    # literal_primitive: INTEGER_LIT | FLOAT_LIT | STRING_LIT | TRUE | FALSE;
    def visitLiteral_primitive(self, ctx: HLangParser.Literal_primitiveContext):
        if ctx.INTEGER_LIT():
            return IntegerLiteral(int(ctx.INTEGER_LIT().getText()))
        if ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        if ctx.STRING_LIT():
            # The lexer rule already strips the quotes
            return StringLiteral(ctx.STRING_LIT().getText())
        if ctx.TRUE() or ctx.FALSE():
            return BooleanLiteral(ctx.getChild(0).getText() == 'true')

    # array_literal: LBRACK list_expression RBRACK;
    def visitArray_literal(self, ctx: HLangParser.Array_literalContext):
        # HLang spec uses a simpler array literal form `[1, 2, 3]`
        if ctx.LBRACK():
            elements = self.visit(ctx.list_expression())
            return ArrayLiteral(elements)
        # The other form `[3]int{...}` is not in spec, ignoring.
        return None