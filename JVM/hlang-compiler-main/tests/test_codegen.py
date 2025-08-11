from src.utils.nodes import *

from utils import CodeGenerator


def test_001():
    """Test basic print statement"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), [StringLiteral("Hello World")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_002_if_else():
    """If/Else with comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
            IfStmt(
                BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(2)),
                ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FAIL")])),
                [],
                ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("OK")]))
            )
                ],
            )
        ],
    )
    expected = "OK"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_002_if_else():
    """If/Else with comparison"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
            IfStmt(
                BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(2)),
                ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FAIL")])),
                [],
                ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("OK")]))
            )
                ],
            )
        ],
    )
    expected = "OK"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_003_if_else_false_branch():
    """If/Else with false branch"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    IfStmt(
                        BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(2)),
                        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FAIL")])),
                        [],
                        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("OK")]))
                    )
                ],
            )
        ],
    )
    expected = "OK"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_004_variable_declaration():
    """Variable declaration and print"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(42)),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
                ],
            )
        ],
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_005_assignment():
    """Assignment updates variable"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    Assignment(IdLValue("x"), IntegerLiteral(99)),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
                ],
            )
        ],
    )
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_006_arithmetic_operation():
    """Addition and multiplication"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(),
                        BinaryOp(IntegerLiteral(3), "+", BinaryOp(IntegerLiteral(4), "*", IntegerLiteral(5)))
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
                ],
            )
        ],
    )
    expected = str(3 + 4 * 5)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_007_while_loop_sum():
    """While loop sum 1..5"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(1)),
                    VarDecl("sum", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<=", IntegerLiteral(5)),
                        BlockStmt([
                            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i"))),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
                ],
            )
        ],
    )
    expected = str(sum(range(1, 6)))
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_008_for_loop_sum():
    """For loop sum array"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("arr", ArrayType(IntType(), 5),
                        ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2),
                                      IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])
                    ),
                    VarDecl("total", IntType(), IntegerLiteral(0)),
                    ForStmt(
                        "x",
                        Identifier("arr"),
                        BlockStmt([
                            Assignment(IdLValue("total"), BinaryOp(Identifier("total"), "+", Identifier("x")))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("total")]))
                ],
            )
        ],
    )
    expected = str(sum([1, 2, 3, 4, 5]))
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_009_function_return():
    """Function returns a value"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("add"), [IntegerLiteral(3), IntegerLiteral(4)])]))
                ],
            ),
            FuncDecl(
                "add",
                [Param("a", IntType()), Param("b", IntType())],
                IntType(),
                [
                    ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
                ]
            )
        ],
    )
    expected = str(3 + 4)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected