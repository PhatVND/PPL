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
    """For loop print sum array"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    # int[] array = [10, 20]
                    VarDecl(
                        "array",
                        ArrayType(IntType(), 2),
                        ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20)])
                    ),
                    # for (a in array) { print("" + a); }
                    ForStmt(
                        "a",
                        Identifier("array"),
                        BlockStmt([
                            ExprStmt(
                                FunctionCall(
                                    Identifier("print"),
                                    [
                                        BinaryOp(
                                            StringLiteral(""),
                                            "+",
                                            Identifier("a")
                                        )
                                    ]
                                )
                            )
                        ])
                    ),
                ],
            )
        ],
    )

    expected = "1020"  # Kết quả in chuỗi "" + 10 + "" + 20
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
def test_010_if_else_max_of_two():
    """If-else chooses max(a, b)"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(17)),
                    VarDecl("b", IntType(), IntegerLiteral(23)),
                    VarDecl("m", IntType(), IntegerLiteral(0)),
                    IfStmt(
                        BinaryOp(Identifier("a"), ">", Identifier("b")),
                        BlockStmt([Assignment(IdLValue("m"), Identifier("a"))]),
                        [],  # <- đây là elifs
                        BlockStmt([Assignment(IdLValue("m"), Identifier("b"))])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("m")]))
                ],
            )
        ],
    )
    expected = str(max(17, 23))
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_011_while_loop_product():
    """While loop computes product 1..4"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(1)),
                    VarDecl("prod", IntType(), IntegerLiteral(1)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<=", IntegerLiteral(4)),
                        BlockStmt([
                            Assignment(IdLValue("prod"), BinaryOp(Identifier("prod"), "*", Identifier("i"))),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("prod")]))
                ],
            )
        ],
    )
    expected = str(1 * 2 * 3 * 4)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_012_function_square():
    """Function square(n) returns n*n"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("square"), [IntegerLiteral(12)])]))
                ],
            ),
            FuncDecl(
                "square",
                [Param("n", IntType())],
                IntType(),
                [
                    ReturnStmt(BinaryOp(Identifier("n"), "*", Identifier("n")))
                ]
            )
        ],
    )
    expected = str(12 * 12)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_013_recursive_factorial():
    """Recursive factorial(5)"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("fact"), [IntegerLiteral(5)])]
                    ))
                ],
            ),
            FuncDecl(
                "fact",
                [Param("n", IntType())],
                IntType(),
                [
                    IfStmt(
                        BinaryOp(Identifier("n"), "<=", IntegerLiteral(1)),
                        BlockStmt([ReturnStmt(IntegerLiteral(1))]),
                        [],  # không có elif
                        BlockStmt([
                            ReturnStmt(
                                BinaryOp(
                                    Identifier("n"),
                                    "*",
                                    FunctionCall(
                                        Identifier("fact"),
                                        [BinaryOp(Identifier("n"), "-", IntegerLiteral(1))]
                                    )
                                )
                            )
                        ])
                    ),
                    ReturnStmt(None)  # 💥 Quan trọng: tránh fall-through để JVM verifier không lỗi
                ]
            )
        ],
    )
    expected = str(120)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected



def test_014_two_for_loops_sum_two_arrays():
    """Two for-in loops sum elements of two arrays"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("a1", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6)])),
                    VarDecl("a2", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(3), IntegerLiteral(5), IntegerLiteral(7)])),
                    VarDecl("total", IntType(), IntegerLiteral(0)),
                    ForStmt(
                        "x",
                        Identifier("a1"),
                        BlockStmt([
                            Assignment(IdLValue("total"), BinaryOp(Identifier("total"), "+", Identifier("x")))
                        ])
                    ),
                    ForStmt(
                        "y",
                        Identifier("a2"),
                        BlockStmt([
                            Assignment(IdLValue("total"), BinaryOp(Identifier("total"), "+", Identifier("y")))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("total")]))
                ],
            )
        ],
    )
    expected = str(sum([2,4,6]) + sum([1,3,5,7]))
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_015_local_shadowing():
    """Local variable shadows outer; print inner value"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(5)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("use_local"), [IntegerLiteral(9)])]))
                ],
            ),
            FuncDecl(
                "use_local",
                [Param("param", IntType())],
                IntType(),
                [
                    # Local x should shadow any outer x
                    VarDecl("x", IntType(), IntegerLiteral(100)),
                    ReturnStmt(BinaryOp(Identifier("x"), "+", Identifier("param")))
                ]
            )
        ],
    )
    expected = str(100 + 9)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_016_nested_if():
    """Nested if computes sign of number"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("sign"), [IntegerLiteral(-7)])]))
                ],
            ),
            FuncDecl(
                "sign",
                [Param("n", IntType())],
                IntType(),
                [
                    IfStmt(
                        BinaryOp(Identifier("n"), "==", IntegerLiteral(0)),
                        BlockStmt([ReturnStmt(IntegerLiteral(0))]),
                        [],  
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("n"), "<", IntegerLiteral(0)),
                                BlockStmt([ReturnStmt(BinaryOp(IntegerLiteral(0), "-", IntegerLiteral(1)))]),  # -1
                                [],  # 💡 thêm dòng này: elifs rỗng
                                BlockStmt([ReturnStmt(IntegerLiteral(1))])
                            )
                        ])
                    )
                ]
            )
        ],
    )
    expected = str(-1)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_017_fibonacci_iterative():
    """Iterative Fibonacci: fib(10) = 55 (starting fib(0)=0, fib(1)=1)"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("n", IntType(), IntegerLiteral(10)),
                    VarDecl("a", IntType(), IntegerLiteral(0)),
                    VarDecl("b", IntType(), IntegerLiteral(1)),
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", Identifier("n")),
                        BlockStmt([
                            VarDecl("tmp", IntType(), BinaryOp(Identifier("a"), "+", Identifier("b"))),
                            Assignment(IdLValue("a"), Identifier("b")),
                            Assignment(IdLValue("b"), Identifier("tmp")),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("a")]))
                ],
            )
        ],
    )
    # fib(10) = 55
    expected = str(55)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_018_sum_mixed_numbers_for_loop():
    """For loop sums mixed positive/negative integers"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl(
                        "arr",
                        ArrayType(IntType(), 6),
                        ArrayLiteral([
                            IntegerLiteral(10),
                            IntegerLiteral(-3),
                            IntegerLiteral(7),
                            IntegerLiteral(-2),
                            IntegerLiteral(0),
                            IntegerLiteral(5),
                        ])
                    ),
                    VarDecl("total", IntType(), IntegerLiteral(0)),
                    ForStmt(
                        "v",
                        Identifier("arr"),
                        BlockStmt([
                            Assignment(IdLValue("total"), BinaryOp(Identifier("total"), "+", Identifier("v")))
                        ])
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("total")]))
                ],
            )
        ],
    )
    expected = str(10 - 3 + 7 - 2 + 0 + 5)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_019_early_return():
    """Function returns early based on condition"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("abs_like"), [IntegerLiteral(-42)])]))
                ],
            ),
            FuncDecl(
                "abs_like",
                [Param("x", IntType())],
                IntType(),
                [
                    IfStmt(
                        BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                        BlockStmt([ReturnStmt(BinaryOp(IntegerLiteral(0), "-", Identifier("x")))]),
                        [],  # ✅ thêm elifs rỗng vào đây
                        BlockStmt([ReturnStmt(Identifier("x"))])
                    )
                ]
            )
        ],
    )
    expected = str(abs(-42))
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_020_return_no_else_branch():
    """Function returns early without else branch"""
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
                            Identifier("print"),
                            [
                                FunctionCall(
                                    Identifier("check_even"),
                                    [IntegerLiteral(6)]
                                )
                            ]
                        )
                    )
                ],
            ),
            FuncDecl(
                "check_even",
                [Param("n", IntType())],
                IntType(),
                [
                    IfStmt(
                        BinaryOp(
                            BinaryOp(Identifier("n"), "%", IntegerLiteral(2)),
                            "==",
                            IntegerLiteral(0)
                        ),
                        BlockStmt([
                            ReturnStmt(IntegerLiteral(1))
                        ]),
                        [],       # <-- elif_branches
                        None      # <-- else_stmt
                    ),
                    ReturnStmt(IntegerLiteral(0))
                ]
            )
        ],
    )

    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_021_nested_function_call():
    """Nested function calls: double(abs_like(-10)) == 20"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [
                        FunctionCall(Identifier("double"), [
                            FunctionCall(Identifier("abs_like"), [IntegerLiteral(-10)])
                        ])
                    ]))
                ],
            ),
            FuncDecl(
                "abs_like",
                [Param("x", IntType())],
                IntType(),
                [
                    IfStmt(
                        BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                        BlockStmt([
                            ReturnStmt(BinaryOp(IntegerLiteral(0), "-", Identifier("x")))
                        ]),
                        [],  # <-- elif_branches
                        BlockStmt([
                            ReturnStmt(Identifier("x"))
                        ])
                    )
                ]
            ),
            FuncDecl(
                "double",
                [Param("y", IntType())],
                IntType(),
                [
                    ReturnStmt(BinaryOp(Identifier("y"), "*", IntegerLiteral(2)))
                ]
            )
        ],
    )
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_022_void_function_call():
    """Call function that returns void and prints from inside"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("hello"), []))
                ],
            ),
            FuncDecl(
                "hello",
                [],
                VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hi")]))
                ]
            )
        ],
    )
    expected = 'Hi'  # vì StringLiteral("Hi") thêm dấu ngoặc kép khi in
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected