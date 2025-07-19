# Generated from d:/StudyingStuffs/ThirdYear/PPL/PPL/NEW/hlang-compiler-main/src/grammar/HLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .HLangParser import HLangParser
else:
    from HLangParser import HLangParser

# This class defines a complete listener for a parse tree produced by HLangParser.
class HLangListener(ParseTreeListener):

    # Enter a parse tree produced by HLangParser#program.
    def enterProgram(self, ctx:HLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by HLangParser#program.
    def exitProgram(self, ctx:HLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by HLangParser#declared_statement_list.
    def enterDeclared_statement_list(self, ctx:HLangParser.Declared_statement_listContext):
        pass

    # Exit a parse tree produced by HLangParser#declared_statement_list.
    def exitDeclared_statement_list(self, ctx:HLangParser.Declared_statement_listContext):
        pass


    # Enter a parse tree produced by HLangParser#literal.
    def enterLiteral(self, ctx:HLangParser.LiteralContext):
        pass

    # Exit a parse tree produced by HLangParser#literal.
    def exitLiteral(self, ctx:HLangParser.LiteralContext):
        pass


    # Enter a parse tree produced by HLangParser#literal_primitive.
    def enterLiteral_primitive(self, ctx:HLangParser.Literal_primitiveContext):
        pass

    # Exit a parse tree produced by HLangParser#literal_primitive.
    def exitLiteral_primitive(self, ctx:HLangParser.Literal_primitiveContext):
        pass


    # Enter a parse tree produced by HLangParser#mytype.
    def enterMytype(self, ctx:HLangParser.MytypeContext):
        pass

    # Exit a parse tree produced by HLangParser#mytype.
    def exitMytype(self, ctx:HLangParser.MytypeContext):
        pass


    # Enter a parse tree produced by HLangParser#primitive_type.
    def enterPrimitive_type(self, ctx:HLangParser.Primitive_typeContext):
        pass

    # Exit a parse tree produced by HLangParser#primitive_type.
    def exitPrimitive_type(self, ctx:HLangParser.Primitive_typeContext):
        pass


    # Enter a parse tree produced by HLangParser#array_type.
    def enterArray_type(self, ctx:HLangParser.Array_typeContext):
        pass

    # Exit a parse tree produced by HLangParser#array_type.
    def exitArray_type(self, ctx:HLangParser.Array_typeContext):
        pass


    # Enter a parse tree produced by HLangParser#array_dimention.
    def enterArray_dimention(self, ctx:HLangParser.Array_dimentionContext):
        pass

    # Exit a parse tree produced by HLangParser#array_dimention.
    def exitArray_dimention(self, ctx:HLangParser.Array_dimentionContext):
        pass


    # Enter a parse tree produced by HLangParser#array_dimention_element.
    def enterArray_dimention_element(self, ctx:HLangParser.Array_dimention_elementContext):
        pass

    # Exit a parse tree produced by HLangParser#array_dimention_element.
    def exitArray_dimention_element(self, ctx:HLangParser.Array_dimention_elementContext):
        pass


    # Enter a parse tree produced by HLangParser#array_literal.
    def enterArray_literal(self, ctx:HLangParser.Array_literalContext):
        pass

    # Exit a parse tree produced by HLangParser#array_literal.
    def exitArray_literal(self, ctx:HLangParser.Array_literalContext):
        pass


    # Enter a parse tree produced by HLangParser#list_array_value.
    def enterList_array_value(self, ctx:HLangParser.List_array_valueContext):
        pass

    # Exit a parse tree produced by HLangParser#list_array_value.
    def exitList_array_value(self, ctx:HLangParser.List_array_valueContext):
        pass


    # Enter a parse tree produced by HLangParser#list_array_value_element.
    def enterList_array_value_element(self, ctx:HLangParser.List_array_value_elementContext):
        pass

    # Exit a parse tree produced by HLangParser#list_array_value_element.
    def exitList_array_value_element(self, ctx:HLangParser.List_array_value_elementContext):
        pass


    # Enter a parse tree produced by HLangParser#list_expression.
    def enterList_expression(self, ctx:HLangParser.List_expressionContext):
        pass

    # Exit a parse tree produced by HLangParser#list_expression.
    def exitList_expression(self, ctx:HLangParser.List_expressionContext):
        pass


    # Enter a parse tree produced by HLangParser#list_expression_prime.
    def enterList_expression_prime(self, ctx:HLangParser.List_expression_primeContext):
        pass

    # Exit a parse tree produced by HLangParser#list_expression_prime.
    def exitList_expression_prime(self, ctx:HLangParser.List_expression_primeContext):
        pass


    # Enter a parse tree produced by HLangParser#expression.
    def enterExpression(self, ctx:HLangParser.ExpressionContext):
        pass

    # Exit a parse tree produced by HLangParser#expression.
    def exitExpression(self, ctx:HLangParser.ExpressionContext):
        pass


    # Enter a parse tree produced by HLangParser#expression1.
    def enterExpression1(self, ctx:HLangParser.Expression1Context):
        pass

    # Exit a parse tree produced by HLangParser#expression1.
    def exitExpression1(self, ctx:HLangParser.Expression1Context):
        pass


    # Enter a parse tree produced by HLangParser#expression2.
    def enterExpression2(self, ctx:HLangParser.Expression2Context):
        pass

    # Exit a parse tree produced by HLangParser#expression2.
    def exitExpression2(self, ctx:HLangParser.Expression2Context):
        pass


    # Enter a parse tree produced by HLangParser#expression3.
    def enterExpression3(self, ctx:HLangParser.Expression3Context):
        pass

    # Exit a parse tree produced by HLangParser#expression3.
    def exitExpression3(self, ctx:HLangParser.Expression3Context):
        pass


    # Enter a parse tree produced by HLangParser#expression4.
    def enterExpression4(self, ctx:HLangParser.Expression4Context):
        pass

    # Exit a parse tree produced by HLangParser#expression4.
    def exitExpression4(self, ctx:HLangParser.Expression4Context):
        pass


    # Enter a parse tree produced by HLangParser#expression5.
    def enterExpression5(self, ctx:HLangParser.Expression5Context):
        pass

    # Exit a parse tree produced by HLangParser#expression5.
    def exitExpression5(self, ctx:HLangParser.Expression5Context):
        pass


    # Enter a parse tree produced by HLangParser#expression6.
    def enterExpression6(self, ctx:HLangParser.Expression6Context):
        pass

    # Exit a parse tree produced by HLangParser#expression6.
    def exitExpression6(self, ctx:HLangParser.Expression6Context):
        pass


    # Enter a parse tree produced by HLangParser#anonymous_function.
    def enterAnonymous_function(self, ctx:HLangParser.Anonymous_functionContext):
        pass

    # Exit a parse tree produced by HLangParser#anonymous_function.
    def exitAnonymous_function(self, ctx:HLangParser.Anonymous_functionContext):
        pass


    # Enter a parse tree produced by HLangParser#arrow_mytype_opt.
    def enterArrow_mytype_opt(self, ctx:HLangParser.Arrow_mytype_optContext):
        pass

    # Exit a parse tree produced by HLangParser#arrow_mytype_opt.
    def exitArrow_mytype_opt(self, ctx:HLangParser.Arrow_mytype_optContext):
        pass


    # Enter a parse tree produced by HLangParser#builtin_func.
    def enterBuiltin_func(self, ctx:HLangParser.Builtin_funcContext):
        pass

    # Exit a parse tree produced by HLangParser#builtin_func.
    def exitBuiltin_func(self, ctx:HLangParser.Builtin_funcContext):
        pass


    # Enter a parse tree produced by HLangParser#expression7.
    def enterExpression7(self, ctx:HLangParser.Expression7Context):
        pass

    # Exit a parse tree produced by HLangParser#expression7.
    def exitExpression7(self, ctx:HLangParser.Expression7Context):
        pass


    # Enter a parse tree produced by HLangParser#function_call.
    def enterFunction_call(self, ctx:HLangParser.Function_callContext):
        pass

    # Exit a parse tree produced by HLangParser#function_call.
    def exitFunction_call(self, ctx:HLangParser.Function_callContext):
        pass


    # Enter a parse tree produced by HLangParser#list_statement.
    def enterList_statement(self, ctx:HLangParser.List_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#list_statement.
    def exitList_statement(self, ctx:HLangParser.List_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#list_statement_prime.
    def enterList_statement_prime(self, ctx:HLangParser.List_statement_primeContext):
        pass

    # Exit a parse tree produced by HLangParser#list_statement_prime.
    def exitList_statement_prime(self, ctx:HLangParser.List_statement_primeContext):
        pass


    # Enter a parse tree produced by HLangParser#statement.
    def enterStatement(self, ctx:HLangParser.StatementContext):
        pass

    # Exit a parse tree produced by HLangParser#statement.
    def exitStatement(self, ctx:HLangParser.StatementContext):
        pass


    # Enter a parse tree produced by HLangParser#increment_statement.
    def enterIncrement_statement(self, ctx:HLangParser.Increment_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#increment_statement.
    def exitIncrement_statement(self, ctx:HLangParser.Increment_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#block_statement.
    def enterBlock_statement(self, ctx:HLangParser.Block_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#block_statement.
    def exitBlock_statement(self, ctx:HLangParser.Block_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#declared_statement.
    def enterDeclared_statement(self, ctx:HLangParser.Declared_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#declared_statement.
    def exitDeclared_statement(self, ctx:HLangParser.Declared_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#while_statement.
    def enterWhile_statement(self, ctx:HLangParser.While_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#while_statement.
    def exitWhile_statement(self, ctx:HLangParser.While_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#variables_declared.
    def enterVariables_declared(self, ctx:HLangParser.Variables_declaredContext):
        pass

    # Exit a parse tree produced by HLangParser#variables_declared.
    def exitVariables_declared(self, ctx:HLangParser.Variables_declaredContext):
        pass


    # Enter a parse tree produced by HLangParser#variables_declared_without_semi_for_loop.
    def enterVariables_declared_without_semi_for_loop(self, ctx:HLangParser.Variables_declared_without_semi_for_loopContext):
        pass

    # Exit a parse tree produced by HLangParser#variables_declared_without_semi_for_loop.
    def exitVariables_declared_without_semi_for_loop(self, ctx:HLangParser.Variables_declared_without_semi_for_loopContext):
        pass


    # Enter a parse tree produced by HLangParser#constants_declared.
    def enterConstants_declared(self, ctx:HLangParser.Constants_declaredContext):
        pass

    # Exit a parse tree produced by HLangParser#constants_declared.
    def exitConstants_declared(self, ctx:HLangParser.Constants_declaredContext):
        pass


    # Enter a parse tree produced by HLangParser#const_type_opt.
    def enterConst_type_opt(self, ctx:HLangParser.Const_type_optContext):
        pass

    # Exit a parse tree produced by HLangParser#const_type_opt.
    def exitConst_type_opt(self, ctx:HLangParser.Const_type_optContext):
        pass


    # Enter a parse tree produced by HLangParser#function_declared.
    def enterFunction_declared(self, ctx:HLangParser.Function_declaredContext):
        pass

    # Exit a parse tree produced by HLangParser#function_declared.
    def exitFunction_declared(self, ctx:HLangParser.Function_declaredContext):
        pass


    # Enter a parse tree produced by HLangParser#generic_parameter_opt.
    def enterGeneric_parameter_opt(self, ctx:HLangParser.Generic_parameter_optContext):
        pass

    # Exit a parse tree produced by HLangParser#generic_parameter_opt.
    def exitGeneric_parameter_opt(self, ctx:HLangParser.Generic_parameter_optContext):
        pass


    # Enter a parse tree produced by HLangParser#generic_parameter_list.
    def enterGeneric_parameter_list(self, ctx:HLangParser.Generic_parameter_listContext):
        pass

    # Exit a parse tree produced by HLangParser#generic_parameter_list.
    def exitGeneric_parameter_list(self, ctx:HLangParser.Generic_parameter_listContext):
        pass


    # Enter a parse tree produced by HLangParser#generic_parameter_list_opt.
    def enterGeneric_parameter_list_opt(self, ctx:HLangParser.Generic_parameter_list_optContext):
        pass

    # Exit a parse tree produced by HLangParser#generic_parameter_list_opt.
    def exitGeneric_parameter_list_opt(self, ctx:HLangParser.Generic_parameter_list_optContext):
        pass


    # Enter a parse tree produced by HLangParser#function_body_container.
    def enterFunction_body_container(self, ctx:HLangParser.Function_body_containerContext):
        pass

    # Exit a parse tree produced by HLangParser#function_body_container.
    def exitFunction_body_container(self, ctx:HLangParser.Function_body_containerContext):
        pass


    # Enter a parse tree produced by HLangParser#parameter_list.
    def enterParameter_list(self, ctx:HLangParser.Parameter_listContext):
        pass

    # Exit a parse tree produced by HLangParser#parameter_list.
    def exitParameter_list(self, ctx:HLangParser.Parameter_listContext):
        pass


    # Enter a parse tree produced by HLangParser#parameter_list_opt.
    def enterParameter_list_opt(self, ctx:HLangParser.Parameter_list_optContext):
        pass

    # Exit a parse tree produced by HLangParser#parameter_list_opt.
    def exitParameter_list_opt(self, ctx:HLangParser.Parameter_list_optContext):
        pass


    # Enter a parse tree produced by HLangParser#parameter_list_prime.
    def enterParameter_list_prime(self, ctx:HLangParser.Parameter_list_primeContext):
        pass

    # Exit a parse tree produced by HLangParser#parameter_list_prime.
    def exitParameter_list_prime(self, ctx:HLangParser.Parameter_list_primeContext):
        pass


    # Enter a parse tree produced by HLangParser#parameter.
    def enterParameter(self, ctx:HLangParser.ParameterContext):
        pass

    # Exit a parse tree produced by HLangParser#parameter.
    def exitParameter(self, ctx:HLangParser.ParameterContext):
        pass


    # Enter a parse tree produced by HLangParser#assignment_statement.
    def enterAssignment_statement(self, ctx:HLangParser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#assignment_statement.
    def exitAssignment_statement(self, ctx:HLangParser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#lhs_assignment_statement.
    def enterLhs_assignment_statement(self, ctx:HLangParser.Lhs_assignment_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#lhs_assignment_statement.
    def exitLhs_assignment_statement(self, ctx:HLangParser.Lhs_assignment_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#assignment_statement_without_semi_for_loop.
    def enterAssignment_statement_without_semi_for_loop(self, ctx:HLangParser.Assignment_statement_without_semi_for_loopContext):
        pass

    # Exit a parse tree produced by HLangParser#assignment_statement_without_semi_for_loop.
    def exitAssignment_statement_without_semi_for_loop(self, ctx:HLangParser.Assignment_statement_without_semi_for_loopContext):
        pass


    # Enter a parse tree produced by HLangParser#if_statement.
    def enterIf_statement(self, ctx:HLangParser.If_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#if_statement.
    def exitIf_statement(self, ctx:HLangParser.If_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#else_if_clause_opt.
    def enterElse_if_clause_opt(self, ctx:HLangParser.Else_if_clause_optContext):
        pass

    # Exit a parse tree produced by HLangParser#else_if_clause_opt.
    def exitElse_if_clause_opt(self, ctx:HLangParser.Else_if_clause_optContext):
        pass


    # Enter a parse tree produced by HLangParser#else_if_clause_list.
    def enterElse_if_clause_list(self, ctx:HLangParser.Else_if_clause_listContext):
        pass

    # Exit a parse tree produced by HLangParser#else_if_clause_list.
    def exitElse_if_clause_list(self, ctx:HLangParser.Else_if_clause_listContext):
        pass


    # Enter a parse tree produced by HLangParser#else_if_clause_content.
    def enterElse_if_clause_content(self, ctx:HLangParser.Else_if_clause_contentContext):
        pass

    # Exit a parse tree produced by HLangParser#else_if_clause_content.
    def exitElse_if_clause_content(self, ctx:HLangParser.Else_if_clause_contentContext):
        pass


    # Enter a parse tree produced by HLangParser#else_clause_opt.
    def enterElse_clause_opt(self, ctx:HLangParser.Else_clause_optContext):
        pass

    # Exit a parse tree produced by HLangParser#else_clause_opt.
    def exitElse_clause_opt(self, ctx:HLangParser.Else_clause_optContext):
        pass


    # Enter a parse tree produced by HLangParser#else_clause.
    def enterElse_clause(self, ctx:HLangParser.Else_clauseContext):
        pass

    # Exit a parse tree produced by HLangParser#else_clause.
    def exitElse_clause(self, ctx:HLangParser.Else_clauseContext):
        pass


    # Enter a parse tree produced by HLangParser#for_statement.
    def enterFor_statement(self, ctx:HLangParser.For_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#for_statement.
    def exitFor_statement(self, ctx:HLangParser.For_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#for_in_loop.
    def enterFor_in_loop(self, ctx:HLangParser.For_in_loopContext):
        pass

    # Exit a parse tree produced by HLangParser#for_in_loop.
    def exitFor_in_loop(self, ctx:HLangParser.For_in_loopContext):
        pass


    # Enter a parse tree produced by HLangParser#break_statement.
    def enterBreak_statement(self, ctx:HLangParser.Break_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#break_statement.
    def exitBreak_statement(self, ctx:HLangParser.Break_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#continue_statement.
    def enterContinue_statement(self, ctx:HLangParser.Continue_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#continue_statement.
    def exitContinue_statement(self, ctx:HLangParser.Continue_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#call_statement.
    def enterCall_statement(self, ctx:HLangParser.Call_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#call_statement.
    def exitCall_statement(self, ctx:HLangParser.Call_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#method_call.
    def enterMethod_call(self, ctx:HLangParser.Method_callContext):
        pass

    # Exit a parse tree produced by HLangParser#method_call.
    def exitMethod_call(self, ctx:HLangParser.Method_callContext):
        pass


    # Enter a parse tree produced by HLangParser#return_statement.
    def enterReturn_statement(self, ctx:HLangParser.Return_statementContext):
        pass

    # Exit a parse tree produced by HLangParser#return_statement.
    def exitReturn_statement(self, ctx:HLangParser.Return_statementContext):
        pass


    # Enter a parse tree produced by HLangParser#return_statement_opt.
    def enterReturn_statement_opt(self, ctx:HLangParser.Return_statement_optContext):
        pass

    # Exit a parse tree produced by HLangParser#return_statement_opt.
    def exitReturn_statement_opt(self, ctx:HLangParser.Return_statement_optContext):
        pass



del HLangParser