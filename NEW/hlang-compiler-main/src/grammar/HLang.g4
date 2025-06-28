grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
prev_token = None

def emit(self):
    tk = self.type

    if tk == self.UNCLOSE_STRING:
        result = super().emit()
        if len(result.text) >= 2 and result.text[-1] == '\n' and result.text[-2] == '\r':
            raise UncloseString(result.text[1:-2])
        elif result.text[-1] == '\n':
            raise UncloseString(result.text[1:-1])
        else:
            raise UncloseString(result.text[1:])
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        raw = result.text[1:] 
        idx = raw.find('\\')
        if idx != -1 and idx + 1 < len(raw):
            raise IllegalEscape(raw[:idx + 2])
        raise IllegalEscape(raw)
    elif tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
    elif tk == self.NEWLINE:
        result = super().emit()
    result = super().emit()
    self.prev_token = result
    return result
}

options{
	language = Python3;
}

/* =========================================================================================== */
///////////////////////////////         L E X E R         ///////////////////////////////////////
/* =========================================================================================== */

// TODO Keywords 3.3.2 pdf --------------------------------------------------------------------------
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOL: 'bool';
CONST: 'const';
CONTINUE: 'continue';
BREAK: 'break';
TRUE: 'true';
FALSE: 'false';
LET: 'let';
VOID: 'void';
WHILE: 'while';
IN: 'in';

NEWLINE: '\r'? '\n' -> skip;

// Arithmethic --------------------------------------------------------------------------
INCREMENT: '++';
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

EQUAL: '==';
NOT_EQUAL: '!=';
LESS: '<';
LESS_EQUAL: '<=';
GREATER: '>';
GREATER_EQUAL: '>=';
PIPELINE: '>>';
ARROW: '->';
AND: '&&';
OR: '||';
NOT: '!';

ASSIGN: '=';
// Removed: ASSIGN_STATE, ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN, MOD_ASSIGN (not in HLang spec)

DOT: '.';

//TODO Separators 3.3.4 pdf --------------------------------------------------------------------------

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
COMMA: ',';
QUESTION: '?';
SEMICOLON: ';';
COLON: ':';

//TODO Identifiers 3.3.1 pdf --------------------------------------------------------------------------
ID: [a-zA-Z_] [a-zA-Z0-9_]*;

//TODO Literals 3.3.5 pdf --------------------------------------------------------------------------
INTEGER_LIT: [0-9]+;

FLOAT_LIT: REAL_NUM (EXPONENT_PART)?;
fragment REAL_NUM:
	[0-9]+ '.' [0-9]*; // Reverted to simpler form as per common spec interpretation
fragment EXPONENT_PART: [eE] [+-]? [0-9]+;

STRING_LIT: '"' CHARACTER* '"' {self.text = self.text[1:-1]};
fragment CHARACTER: (~["\\\r\n\u0080-\uFFFF] | ESCAPED_SEQ);

fragment ESCAPED_SEQ: '\\n' | '\\t' | '\\r' | '\\"' | '\\\\';

//TODO skip 3.1 and 3.2 pdf --------------------------------------------------------------------------
WS: [ \t\f\r]+ -> skip;

//TODO Comment 3.2 pdf --------------------------------------------------------------------------
COMMENT_INLINE: '//' (~[\n\r])* -> skip;
COMMENT_BLOCK:
	'/*' (COMMENT_BLOCK | COMMENT_INLINE | (.))*? '*/' -> skip;

//TODO ERROR pdf BTL1 + lexererr.py -------------------------------------------------------------------
ERROR_CHAR: . {raise ErrorToken(self.text)};

UNCLOSE_STRING: '"' CHARACTER* ('\r\n' | '\n' | EOF);

ILLEGAL_ESCAPE: '"' (~["\\\r\n] | ESCAPED_SEQ)* '\\' ~[ntr"\\];

/*----------------------------------        END LEXER         ------------------------------------ */
/* =========================================================================================== */

/* =========================================================================================== */
///////////////////////////////         N E W 		U P D A T E           ///////////////////////////////////////

/* 
 
 ADD INCREMENT_STATEMENT: ++
 
 ADD
 BLOCK_STATEMENT
 
 SỬA variables_declared, để cho có
 trường hợp let ID : string;
 
 Thêm trường hợp user.method();
 Thêm dạng IF "?" a = b? "yes" "no"
 Add gọi hàm, ví dụ str(123)
 Add thêm builtin-function
 */
/* =========================================================================================== */

/* =========================================================================================== */
///////////////////////////////         P A S E R           ///////////////////////////////////////
/* =========================================================================================== */

// Program definition --------------------------------------------------------------------------
program: declared_statement_list EOF;

declared_statement_list: (declared_statement | statement) declared_statement_list
	| (declared_statement | statement);
//TODO Literal 6.6 pdf --------------------------------------------------------------------------
literal: literal_primitive | array_literal;
// struct_lit_instance removed as struct_declared is removed --- ADD NEW ARRAY_LITERAL

literal_primitive:
	INTEGER_LIT
	| FLOAT_LIT
	| STRING_LIT
	| TRUE
	| FALSE;
// NIL removed as not in spec

// NEW UPDATE, FUNCTION_TYPE HERE
mytype:
	ID
	| primitive_type
	| array_type
	| LPAREN mytype RPAREN
	| mytype ARROW mytype;

primitive_type: INT | FLOAT | BOOL | STRING | VOID;
array_type: (array_dimention) (ID | primitive_type)
	| LBRACK mytype SEMICOLON INTEGER_LIT RBRACK (
		array_dimention
	)?;
array_dimention: (array_dimention_element) (array_dimention)
	| array_dimention_element;
array_dimention_element:
	LBRACK INTEGER_LIT RBRACK; // ID removed, only INTEGER_LIT for size

// array_lit_instance -> array_literal, add Dạng [1, 2, 3]
// array_literal:
// 	LBRACK (expression (COMMA expression)*)? RBRACK // Dạng [1,2,3]
// 	| array_type LBRACE (expression (COMMA expression)*)? RBRACE;

// array_literal: ebnf -> bnf
array_literal:
	LBRACK list_expression RBRACK // Dạng [1,2,3]
	| array_type LBRACE list_expression RBRACE; // Dạng [3]int{1,2,3}

// Array_type + giá trị // Example:  [2][3]int {{1,2,3}, {4,5,6}
list_array_value: (list_array_value_element) COMMA (
		list_array_value
	)
	| (list_array_value_element);
list_array_value_element:
	ID
	| literal_primitive
	| LBRACE list_array_value RBRACE;

// Removed struct_lit_instance and all related struct literal rules (not in spec)

// TODO 5.2 Expressions 6 pdf ---------------------------------------------------------------------
list_expression: list_expression_prime |;
list_expression_prime:
	expression COMMA list_expression_prime
	| expression;
// ADD PIPELINE
expression:
	expression PIPELINE expression1
	| expression OR expression1
	| expression1 QUESTION expression COLON expression
	| expression1;
expression1: expression1 AND expression2 | expression2;
expression2:
	expression2 EQUAL expression3
	| expression2 NOT_EQUAL expression3
	| expression2 LESS expression3
	| expression2 LESS_EQUAL expression3
	| expression2 GREATER expression3
	| expression2 GREATER_EQUAL expression3
	| expression3;
expression3:
	expression3 ADD expression4
	| expression3 SUB expression4
	| expression4;
expression4:
	expression4 MUL expression5
	| expression4 DIV expression5
	| expression4 MOD expression5
	| expression5;
expression5:
	INCREMENT expression5
	| NOT expression5
	| SUB expression5
	| expression6;
expression6:
	expression6 (
		LBRACK expression RBRACK
	) // 6.4 pdf --> Accessing array elements. VD:  a[2][3], b[4] ...
	| function_call // Function call
	| expression6 DOT ID
	| expression6 DOT ID LPAREN list_expression RPAREN
	| builtin_func LPAREN list_expression RPAREN
	| ID LPAREN list_expression RPAREN
	| ID
	| primitive_type
	| anonymous_function
	| literal
	| expression7;
// HÀM KHÔNG TÊN

anonymous_function:
	FUNC parameter_list arrow_mytype_opt function_body_container;
arrow_mytype_opt: ARROW mytype |;
// builtin-function
builtin_func: INT | FLOAT | 'STR' | BOOL | ID;
expression7: LPAREN expression RPAREN;

function_call:
	ID LPAREN list_expression RPAREN; // 6.7.1 Function call

// Removed method_call and temp_expression6 rules (not in spec)

//TODO Statement 5 and 4 pdf ----------------------------------------------------------------------
list_statement: list_statement_prime |;
list_statement_prime: (
		statement list_statement_prime
		| statement
	)?;

statement:
	declared_statement
	| assignment_statement
	| if_statement
	| for_statement
	| while_statement
	| break_statement
	| continue_statement
	| call_statement
	| increment_statement
	| block_statement
	| return_statement;

// ADD INCREMENT_STATEMENT, BLOCK_STATEMENT
increment_statement: INCREMENT ID SEMICOLON;
block_statement: function_body_container;
//TODO declared_statement --------------------------------------------------------------------------
declared_statement:
	variables_declared
	| constants_declared
	| function_declared;
// Removed method_declared, struct_declared, interface_declared (not in spec)

// Add while statement
while_statement:
	WHILE LPAREN expression RPAREN function_body_container;

// variables_declared:
// 	LET ID (
// 		COLON mytype (ASSIGN expression)? 
// 		| ASSIGN expression
// 	) SEMICOLON;
variables_declared:
	LET ID (
		COLON mytype ASSIGN expression 
		| ASSIGN expression
	) SEMICOLON;
// update variable in for loop
// variables_declared_without_semi_for_loop:
// 	LET ID mytype? ASSIGN expression; 
variables_declared_without_semi_for_loop:
	ID ASSIGN expression; 

//update constants_declared
// constants_declared:
// 	CONST ID (COLON mytype)? ASSIGN expression SEMICOLON?;
constants_declared:
	CONST ID const_type_opt ASSIGN expression SEMICOLON;
const_type_opt: COLON mytype |; // Optional type for constants

//update function_declared
// function_declared:
// 	FUNC ID generic_parameter_list? parameter_list (ARROW mytype)? function_body_container SEMICOLON?;
// generic_parameter_list: LESS ID (COMMA ID)* GREATER;

function_declared:
	FUNC ID generic_parameter_opt parameter_list arrow_mytype_opt function_body_container SEMICOLON?;
generic_parameter_opt: generic_parameter_list |; // Optional generic parameters
generic_parameter_list: LESS ID generic_parameter_list_opt GREATER;
generic_parameter_list_opt: COMMA ID generic_parameter_list_opt |; // Optional additional generic parameters

function_body_container: LBRACE list_statement_prime RBRACE;

// New parameter rule for functions
// update parameter_list
// parameter_list: LPAREN (parameter (COMMA parameter)*)? RPAREN;
parameter_list: LPAREN parameter_list_opt RPAREN;
parameter_list_opt: parameter parameter_list_prime | ;
parameter_list_prime: COMMA parameter parameter_list_prime | ;
parameter: ID COLON mytype;

//TODO assign_statement --------------------------------------------------------------------------
assignment_statement: (lhs_assignment_statement) ASSIGN (
		expression
	) SEMICOLON; // Only ASSIGN allowed
// assignment_operator rule removed as only ASSIGN is allowed.

lhs_assignment_statement:
	ID
	| lhs_assignment_statement (LBRACK expression RBRACK);
// lhs_assignment_statement DOT ID removed (as structs are removed)

assignment_statement_without_semi_for_loop:
	ID ASSIGN (expression); // Only ASSIGN allowed

// TODO if_statement: --------------------------------------------------------------------------
// update if_statement
// if_statement:
// 	IF (LPAREN expression RPAREN) (function_body_container) (
// 		else_if_clause
// 	)? (else_clause)?; // SEMICOLON removed
// else_if_clause: (else_if_clause_content) else_if_clause
// 	| (else_if_clause_content);
// else_if_clause_content:
// 	ELSE IF (LPAREN expression RPAREN) (function_body_container);

// else_clause: ELSE function_body_container;

if_statement:
	IF (LPAREN expression RPAREN) (function_body_container) else_if_clause_opt else_clause_opt; // SEMICOLON removed
else_if_clause_opt: else_if_clause_list |;
else_if_clause_list: (else_if_clause_content) else_if_clause_list
	| (else_if_clause_content);
else_if_clause_content:
	ELSE IF (LPAREN expression RPAREN) (function_body_container);

else_clause_opt: else_clause |; // Optional else clause
else_clause: ELSE function_body_container;

// TODO for_statement: --------------------------------------------------------------------------
for_statement: for_in_loop; // Simplified to only for-in loop

// New rule for for-in loop as per HLang spec
for_in_loop:
	FOR LPAREN ID IN expression RPAREN function_body_container;
// Removed initialization_for_loop, basic_for_loop, array_for_loop (not in spec)

// TODO break_statement: ------------------------------------------------------------------------
break_statement: BREAK SEMICOLON;

// TODO continue_statement: ---------------------------------------------------------------------
continue_statement: CONTINUE SEMICOLON;

// TODO call_statement: --------------------------------------------------------------------------
call_statement: expression6 SEMICOLON; // ADD expression 6

// TODO return_statement: ------------------------------------------------------------------------
// update return_statement
// return_statement: RETURN expression? SEMICOLON;
return_statement: RETURN return_statement_opt SEMICOLON;
return_statement_opt: expression |; // Optional return expression

/*----------------------------------        END PARSER         ------------------------------------ */
/* ============================================================================================= */