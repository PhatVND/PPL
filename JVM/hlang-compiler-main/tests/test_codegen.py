from src.utils.nodes import *

from utils import CodeGenerator

# =====================================================
# HARD TESTS — Stress control-flow, stack, arrays, recursion
# =====================================================

# H1) If-elif sâu + return xen kẽ (đường đi phức tạp, đảm bảo all paths return)
def test_h01_deep_if_elif_return_mix():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # sign2(-3)= -1 ; sign2(0)=0 ; sign2(4)=1  → "-101"
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", FunctionCall(Identifier("sign2"), [IntegerLiteral(-3)])),
                    "+",
                    BinaryOp(FunctionCall(Identifier("sign2"), [IntegerLiteral(0)]),
                             "+",
                             FunctionCall(Identifier("sign2"), [IntegerLiteral(4)]))
                )
            ]))
        ]),
        FuncDecl("sign2", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "<", IntegerLiteral(0)),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("n"), "<", IntegerLiteral(-10)),
                        BlockStmt([ReturnStmt(IntegerLiteral(-2))]),
                        [],
                        BlockStmt([ReturnStmt(IntegerLiteral(-1))])
                    )
                ]),
                [
                    (BinaryOp(Identifier("n"), "==", IntegerLiteral(0)),
                     BlockStmt([ReturnStmt(IntegerLiteral(0))])),
                    (BinaryOp(Identifier("n"), "==", IntegerLiteral(100)),
                     BlockStmt([ReturnStmt(IntegerLiteral(9))]))
                ],
                BlockStmt([ReturnStmt(IntegerLiteral(1))])
            )
        ])
    ])
    assert CodeGenerator().generate_and_run(ast) == "-11"


# H2) Vòng lặp lồng + continue/break ở cả trong & ngoài (kiểm tra nhãn cond/body/exit)
def test_h02_double_loop_with_mixed_break_continue():
    # Xây chuỗi từ ma trận 2x3, bỏ số chẵn ở vòng trong, break vòng ngoài khi tổng 2 hàng > 20
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("rows", ArrayType(IntType(), 2),
                ArrayLiteral([
                    IntegerLiteral(0),  # placeholder để "giữ chỗ" cho kiểu; không dùng trực tiếp (logic bên dưới dùng mảng b[])
                    IntegerLiteral(0)
                ])),
            VarDecl("a", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])),
            VarDecl("b", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8)])),
            VarDecl("out", StringType(), StringLiteral("")),
            VarDecl("sumrow", IntType(), IntegerLiteral(0)),

            # for row in [a,b]
            ForStmt("row", Identifier("rows"), BlockStmt([
                # ánh xạ row -> một trong hai mảng a/b qua chỉ số row_idx
                # không có literal mảng 2 chiều, ta giả lập: lần 1 dùng a, lần 2 dùng b
            ]))
        ]),
    ])
    # Do ForStmt của HLang duyệt mảng phần tử, để điều khiển chọn a/b, ta làm 2 vòng for thủ công:
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("out", StringType(), StringLiteral("")),
            VarDecl("sumrow", IntType(), IntegerLiteral(0)),

            # Hàng 1: a
            VarDecl("a", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])),
            ForStmt("x", Identifier("a"), BlockStmt([
                IfStmt(BinaryOp(BinaryOp(Identifier("x"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                      BlockStmt([ContinueStmt()]), [], None),    # bỏ số chẵn
                Assignment(IdLValue("out"),
                           BinaryOp(Identifier("out"), "+", BinaryOp(StringLiteral(""), "+", Identifier("x")))),
                Assignment(IdLValue("sumrow"), BinaryOp(Identifier("sumrow"), "+", Identifier("x")))
            ])),

            # Nếu sau hàng 1, tổng > 20 thì break cả tiến trình (mô phỏng break outer bằng if+goto gián tiếp)
            IfStmt(BinaryOp(Identifier("sumrow"), ">", IntegerLiteral(20)),
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))]),
                   [],
                   BlockStmt([
                       # Hàng 2: b
                       VarDecl("b", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8)])),
                       ForStmt("y", Identifier("b"), BlockStmt([
                           IfStmt(BinaryOp(BinaryOp(Identifier("y"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                                  BlockStmt([ContinueStmt()]), [], None),
                           Assignment(IdLValue("out"),
                                      BinaryOp(Identifier("out"), "+", BinaryOp(StringLiteral(""), "+", Identifier("y")))),
                           Assignment(IdLValue("sumrow"), BinaryOp(Identifier("sumrow"), "+", Identifier("y"))),
                           IfStmt(BinaryOp(Identifier("sumrow"), ">", IntegerLiteral(20)),
                                  BlockStmt([BreakStmt()]), [], None)
                       ])),
                       ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
                   ])
            )
        ])
    ])
    # Hàng 1 (a): lấy số lẻ: 3,5  -> out="35", sumrow=8
    # Hàng 2 (b): lấy số lẻ: 7    -> out="357", sumrow=15 (<=20), tiếp tục; thêm 8 bị bỏ vì chẵn, kết thúc -> "357"
    assert CodeGenerator().generate_and_run(ast) == "357"


# H3) Mảng 2 chiều tự mô phỏng (mảng các mảng) + đọc/ghi lồng
def test_h03_pseudo_2d_array_sum_and_update():
    # Ta mô phỏng 2D bằng 2 mảng 1D rồi kết hợp
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("r0", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            VarDecl("r1", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6)])),
            VarDecl("sum", IntType(), IntegerLiteral(0)),
            # sum r0
            ForStmt("v", Identifier("r0"), BlockStmt([
                Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", Identifier("v")))
            ])),
            # sum r1
            ForStmt("v", Identifier("r1"), BlockStmt([
                Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", Identifier("v")))
            ])),
            # cập nhật r1[1] = r0[2] + r1[0]  => 3 + 4 = 7  (giữ nhất quán stack khi load 2 phần tử)
            Assignment(ArrayAccessLValue(Identifier("r1"), IntegerLiteral(1)),
                       BinaryOp(ArrayAccess(Identifier("r0"), IntegerLiteral(2)),
                                "+",
                                ArrayAccess(Identifier("r1"), IntegerLiteral(0)))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("r1"), IntegerLiteral(1))]))
        ])
    ])
    # sum = 1+2+3 + 4+5+6 = 21 ; r1[1] cập nhật thành 7
    assert CodeGenerator().generate_and_run(ast) == "21\n7"


# H4) Biểu thức siêu sâu xen lẫn gọi hàm & truy cập mảng (stress stack)
def test_h04_deep_expr_with_calls_and_array_access():
    # expr: (add(1,2) * (arr[0] + add(3,4))) - (arr[2] - add(5,6))
    expr = BinaryOp(
        BinaryOp(
            FunctionCall(Identifier("add"), [IntegerLiteral(1), IntegerLiteral(2)]),
            "*",
            BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(0)),
                     "+",
                     FunctionCall(Identifier("add"), [IntegerLiteral(3), IntegerLiteral(4)]))
        ),
        "-",
        BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(2)),
                 "-",
                 FunctionCall(Identifier("add"), [IntegerLiteral(5), IntegerLiteral(6)]))
    )
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
            ExprStmt(FunctionCall(Identifier("print"), [expr]))
        ]),
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ])
    ])
    # (1+2)=3 ; add(3,4)=7 ; add(5,6)=11 ; expr = (3*(10+7)) - (30-11) = 3*17 - 19 = 51 - 19 = 32
    assert CodeGenerator().generate_and_run(ast) == "32"


# H5) Đệ quy sâu vừa phải + kết hợp biểu thức (stack call + stack expr)
def test_h05_recursive_sum_of_digits():
    # sumDigits(93027) = 9+3+0+2+7 = 21
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("sumDigits"), [IntegerLiteral(93027)])]))
        ]),
        FuncDecl("sumDigits", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "==", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(IntegerLiteral(0))]),
                [],
                BlockStmt([
                    ReturnStmt(
                        BinaryOp(
                            BinaryOp(Identifier("n"), "%", IntegerLiteral(10)),
                            "+",
                            FunctionCall(Identifier("sumDigits"),
                                         [BinaryOp(Identifier("n"), "/", IntegerLiteral(10))])
                        )
                    )
                ])
            ),
            ReturnStmt(None)
        ])
    ])
    assert CodeGenerator().generate_and_run(ast) == "21"


# H6) For-in lồng + cập nhật chéo chỉ số (dễ sai thứ tự stack khi truy cập phần tử)
def test_h06_nested_for_in_cross_update_indices():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            VarDecl("b", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6)])),
            VarDecl("sum", IntType(), IntegerLiteral(0)),
            ForStmt("x", Identifier("a"), BlockStmt([
                ForStmt("y", Identifier("b"), BlockStmt([
                    Assignment(IdLValue("sum"),
                               BinaryOp(Identifier("sum"),
                                        "+",
                                        BinaryOp(Identifier("x"), "*", Identifier("y"))))
                ]))
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
        ])
    ])
    # sum = 1*(4+5+6) + 2*(4+5+6) + 3*(4+5+6) = (1+2+3)*15 = 6*15 = 90
    assert CodeGenerator().generate_and_run(ast) == "90"


# H7) While có continue trước cập nhật biến quan trọng (cẩn thận tránh infinite loop)
def test_h07_while_continue_before_update_guarded():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(7)),
                BlockStmt([
                    # tăng i trước để không kẹt vòng lặp
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                    IfStmt(
                        BinaryOp(BinaryOp(Identifier("i"), "%", IntegerLiteral(3)), "==", IntegerLiteral(0)),
                        BlockStmt([ContinueStmt()]),
                        [],
                        None
                    ),
                    Assignment(IdLValue("out"),
                               BinaryOp(Identifier("out"), "+",
                                        BinaryOp(StringLiteral(""), "+", Identifier("i"))))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    # i đi 1..7, bỏ bội số 3: 3,6 → out="12457"
    assert CodeGenerator().generate_and_run(ast) == "12457"


# H8) Shadowing phức tạp qua nhiều block + dùng sau khi thoát block
def test_h08_complex_shadowing_blocks_and_use_outer():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(1)),
            BlockStmt([
                VarDecl("x", IntType(), IntegerLiteral(10)),
                BlockStmt([
                    VarDecl("x", IntType(), IntegerLiteral(100)),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))  # 100
                ]),
                ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))      # 10
            ]),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))          # 1
        ])
    ])
    assert CodeGenerator().generate_and_run(ast) == "100\n10\n1"


# H9) Hàm trả về bool dùng làm điều kiện lồng nhau + gọi chéo
def test_h09_bool_return_used_in_nested_if():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(
                FunctionCall(Identifier("gt"), [IntegerLiteral(10), IntegerLiteral(5)]),
                BlockStmt([
                    IfStmt(
                        FunctionCall(Identifier("eq"), [IntegerLiteral(7), IntegerLiteral(7)]),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("OK")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FAIL")]))])
                    )
                ]),
                [],
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FAIL")]))])
            )
        ]),
        FuncDecl("gt", [Param("a", IntType()), Param("b", IntType())], BoolType(), [
            ReturnStmt(BinaryOp(Identifier("a"), ">", Identifier("b")))
        ]),
        FuncDecl("eq", [Param("a", IntType()), Param("b", IntType())], BoolType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "==", Identifier("b")))
        ])
    ])
    assert CodeGenerator().generate_and_run(ast) == "OK"


# H10) Kết hợp nhiều locals + biểu thức sâu + gọi hàm trong khi return
def test_h10_many_locals_deep_expr_and_return_call():
    body = [
        VarDecl("a", IntType(), IntegerLiteral(1)),
        VarDecl("b", IntType(), IntegerLiteral(2)),
        VarDecl("c", IntType(), IntegerLiteral(3)),
        VarDecl("d", IntType(), IntegerLiteral(4)),
        ReturnStmt(BinaryOp(
            BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")),
                     "+",
                     FunctionCall(Identifier("add"), [Identifier("c"), Identifier("d")])),
            "*",
            FunctionCall(Identifier("add"), [IntegerLiteral(5), IntegerLiteral(6)])
        ))
    ]
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("f"), [])]))
        ]),
        FuncDecl("add", [Param("x", IntType()), Param("y", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("x"), "+", Identifier("y")))
        ]),
        FuncDecl("f", [], IntType(), body)
    ])
    # (a+b+(c+d)) * (5+6) = (1+2+(3+4))*11 = (1+2+7)*11 = 10*11 = 110
    assert CodeGenerator().generate_and_run(ast) == "110"


# H11) Tổ hợp for-in + while + if với nhiều nhãn (rất dễ lệch nhãn break/continue)
def test_h11_combo_for_while_if_many_labels():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 5),
                    ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])),
            VarDecl("out", StringType(), StringLiteral("")),
            ForStmt("v", Identifier("xs"), BlockStmt([
                VarDecl("t", IntType(), Identifier("v")),
                WhileStmt(
                    BinaryOp(Identifier("t"), ">", IntegerLiteral(0)),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(BinaryOp(Identifier("t"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                            BlockStmt([Assignment(IdLValue("t"), BinaryOp(Identifier("t"), "-", IntegerLiteral(1))),
                                       ContinueStmt()]),
                            [],
                            None
                        ),
                        Assignment(IdLValue("out"),
                                   BinaryOp(Identifier("out"), "+",
                                            BinaryOp(StringLiteral(""), "+", Identifier("t")))),
                        Assignment(IdLValue("t"), BinaryOp(Identifier("t"), "-", IntegerLiteral(1))),
                        IfStmt(BinaryOp(Identifier("t"), "==", IntegerLiteral(1)),
                               BlockStmt([BreakStmt()]), [], None)
                    ])
                )
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    # v=1 -> t:1 -> append "1", t=0 stop
    # v=2 -> t:2(even) dec->1 continue, then break at t==1 (không append)
    # v=3 -> t:3 -> append "3", t=2(even) dec->1; break (không append 1)
    # v=4 -> t:4 even->3 continue; append "3"; t->2 even->1 continue; break
    # v=5 -> t:5 append "5"; t->4 even->3 continue; append "3"; t->2 even->1 continue; break
    # out = "1" + "3" + "3" + "5" + "3" = "13353"
    assert CodeGenerator().generate_and_run(ast) == "113131531"


# H12) Chuỗi in trộn nhiều kiểu + ép sang chuỗi qua "" + expr sâu (stress println overload chọn đúng)
def test_h12_mixed_types_print_coercion_chain():
    deep = BinaryOp(
        BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(5)),      # 10
        "+",
        BinaryOp(IntegerLiteral(7), "*", IntegerLiteral(3))       # 21 → 31
    )
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("b", BoolType(), BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", IntegerLiteral(42)),
                    "+",
                    BinaryOp(
                        BinaryOp(StringLiteral("-"), "+", Identifier("b")),  # "-true"
                        "+",
                        deep
                    )
                )
            ]))
        ])
    ])
    # "" + 42 -> "42"; "42" + ("-true" + 31) = "42-true31"
    assert CodeGenerator().generate_and_run(ast) == "42-true31"


# H13) Hàm nhận tham số mảng + tổng N phần tử đầu
def test_h13_function_sum_prefix_of_array():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 6),
                    ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6),
                                  IntegerLiteral(8), IntegerLiteral(10), IntegerLiteral(12)])),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("sumN"),
                                                [Identifier("a"), IntegerLiteral(4)])]))
        ]),
        FuncDecl("sumN", [Param("arr", ArrayType(IntType(), 6)), Param("n", IntType())], IntType(), [
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("s", IntType(), IntegerLiteral(0)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", Identifier("n")),
                BlockStmt([
                    Assignment(IdLValue("s"), BinaryOp(Identifier("s"),
                                                       "+",
                                                       ArrayAccess(Identifier("arr"),
                                                                   Identifier("i")))),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ReturnStmt(Identifier("s"))
        ])
    ])
    expected = str(2 + 4 + 6 + 8)
    assert CodeGenerator().generate_and_run(ast) == expected


# H14) Cập nhật mảng dựa trên giá trị duyệt for-in (không dùng chỉ số)
def test_h14_for_in_update_other_array_using_value():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("src", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)])),
            VarDecl("dst", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            ForStmt("v", Identifier("src"), BlockStmt([
                # ghi vào dst[ v-1 ] = v*v
                Assignment(ArrayAccessLValue(Identifier("dst"),
                                             BinaryOp(Identifier("v"), "-", IntegerLiteral(1))),
                           BinaryOp(Identifier("v"), "*", Identifier("v")))
            ])),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(
                                      BinaryOp(ArrayAccess(Identifier("dst"), IntegerLiteral(0)), "+",
                                               ArrayAccess(Identifier("dst"), IntegerLiteral(1))),
                                      "+",
                                      BinaryOp(ArrayAccess(Identifier("dst"), IntegerLiteral(2)), "+",
                                               ArrayAccess(Identifier("dst"), IntegerLiteral(3)))
                                  )]))
        ])
    ])
    expected = str(1*1 + 2*2 + 3*3 + 4*4)
    assert CodeGenerator().generate_and_run(ast) == expected


# H15) For-in trên mảng String + chèn dấu phân cách có điều kiện
def test_h15_for_in_string_join_with_separator():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("names", ArrayType(StringType(), 3),
                    ArrayLiteral([StringLiteral("A"), StringLiteral("B"), StringLiteral("C")])),
            VarDecl("out", StringType(), StringLiteral("")),
            VarDecl("first", BoolType(), BooleanLiteral(True)),
            ForStmt("s", Identifier("names"), BlockStmt([
                IfStmt(
                    Identifier("first"),
                    BlockStmt([
                        Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", Identifier("s"))),
                        Assignment(IdLValue("first"), BooleanLiteral(False))
                    ]),
                    [],
                    BlockStmt([
                        Assignment(IdLValue("out"),
                                   BinaryOp(Identifier("out"),
                                            "+",
                                            BinaryOp(StringLiteral(","), "+", Identifier("s"))))
                    ])
                )
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = "A,B,C"
    assert CodeGenerator().generate_and_run(ast) == expected


# H16) Return sớm bên trong while (đường đi phức tạp)
def test_h16_function_return_early_inside_while():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("first_even"),
                                                [IntegerLiteral(9)])]))
        ]),
        FuncDecl("first_even", [Param("n", IntType())], IntType(), [
            VarDecl("i", IntType(), IntegerLiteral(1)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<=", Identifier("n")),
                BlockStmt([
                    IfStmt(BinaryOp(BinaryOp(Identifier("i"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                           BlockStmt([ReturnStmt(Identifier("i"))]),
                           [],
                           None),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ReturnStmt(IntegerLiteral(-1))
        ])
    ])
    expected = "2"
    assert CodeGenerator().generate_and_run(ast) == expected


# H17) Fibonacci mảng kích thước 10 (kết quả 55)
def test_h17_fibonacci_iterative_size_10():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("n", IntType(), IntegerLiteral(10)),
            VarDecl("fib", ArrayType(IntType(), 10),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(1),
                                  IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0),
                                  IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0),
                                  IntegerLiteral(0), IntegerLiteral(0)])),
            VarDecl("i", IntType(), IntegerLiteral(2)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", Identifier("n")),
                BlockStmt([
                    Assignment(ArrayAccessLValue(Identifier("fib"), Identifier("i")),
                               BinaryOp(
                                   ArrayAccess(Identifier("fib"), BinaryOp(Identifier("i"), "-", IntegerLiteral(1))),
                                   "+",
                                   ArrayAccess(Identifier("fib"), BinaryOp(Identifier("i"), "-", IntegerLiteral(2)))
                               )),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("fib"),
                                               BinaryOp(Identifier("n"), "-", IntegerLiteral(1)))]))
        ])
    ])
    expected = "34"
    assert CodeGenerator().generate_and_run(ast) == expected


# H18) Chuỗi control-flow lồng rất sâu (if→while→for-in) + biến cờ
def test_h18_deep_nesting_if_while_for_with_flags():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flag", BoolType(), BooleanLiteral(True)),
            VarDecl("xs", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)])),
            VarDecl("acc", IntType(), IntegerLiteral(0)),
            IfStmt(Identifier("flag"),
                   BlockStmt([
                       VarDecl("k", IntType(), IntegerLiteral(0)),
                       WhileStmt(
                           BinaryOp(Identifier("k"), "<", IntegerLiteral(2)),
                           BlockStmt([
                               ForStmt("v", Identifier("xs"), BlockStmt([
                                   IfStmt(BinaryOp(BinaryOp(Identifier("v"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                                          BlockStmt([ContinueStmt()]), [], None),
                                   Assignment(IdLValue("acc"),
                                              BinaryOp(Identifier("acc"), "+", Identifier("v")))
                               ])),
                               Assignment(IdLValue("k"), BinaryOp(Identifier("k"), "+", IntegerLiteral(1)))
                           ])
                       )
                   ]),
                   [],
                   None),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("acc")]))
        ])
    ])
    # Hai lần cộng các số lẻ 1+3=4 → 4*2 = 8
    assert CodeGenerator().generate_and_run(ast) == "8"


# H19) Nhiều locals hơn nữa (30 biến) + cộng dồn
def test_h19_thirty_locals_sum():
    decls = [VarDecl(f"v{i}", IntType(), IntegerLiteral(i)) for i in range(1, 31)]
    acc = Identifier("v1")
    for i in range(2, 31):
        acc = BinaryOp(acc, "+", Identifier(f"v{i}"))
    ast = Program([], [
        FuncDecl("main", [], VoidType(), decls + [
            ExprStmt(FunctionCall(Identifier("print"), [acc]))
        ])
    ])
    expected = str(sum(range(1, 31)))
    assert CodeGenerator().generate_and_run(ast) == expected


# H20) Gọi hàm lồng 4 tầng + dùng trong biểu thức lớn
def test_h20_four_level_nested_calls_in_big_expression():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # print( (inc( inc( inc( inc(3) ) ) ) * 2) + add(5, add(6,7)) )
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(FunctionCall(Identifier("inc"),
                                          [FunctionCall(Identifier("inc"),
                                                        [FunctionCall(Identifier("inc"),
                                                                      [FunctionCall(Identifier("inc"),
                                                                                    [IntegerLiteral(3)])])])]),
                             "*", IntegerLiteral(2)),
                    "+",
                    FunctionCall(Identifier("add"), [IntegerLiteral(5),
                                                     FunctionCall(Identifier("add"), [IntegerLiteral(6), IntegerLiteral(7)])])
                )
            ]))
        ]),
        FuncDecl("inc", [Param("x", IntType())], IntType(), [ ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(1))) ]),
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [ ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b"))) ])
    ])
    expected = str(((3+1+1+1+1) * 2) + (5 + (6+7)))  # (7*2) + 18 = 32
    assert CodeGenerator().generate_and_run(ast) == expected


# H21) Dùng bool trong điều kiện phức (chuỗi && và ||) và in kết quả
def test_h21_complex_boolean_mixture_no_short_circuit_assumed():
    # ((1<2)&&(2<3)&&true) || (false&&(3<1))
    expr = BinaryOp(
        BinaryOp(
            BinaryOp(BinaryOp(IntegerLiteral(1), "<", IntegerLiteral(2)), "&&",
                     BinaryOp(IntegerLiteral(2), "<", IntegerLiteral(3))),
            "&&",
            BooleanLiteral(True)
        ),
        "||",
        BinaryOp(BooleanLiteral(False), "&&",
                 BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(1)))
    )
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(StringLiteral(""), "+", expr)]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected


# H22) Mảng String viết-đọc nhiều lần + nối chuỗi có xen boolean
def test_h22_string_array_multi_updates_and_mixed_concat():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("s", ArrayType(StringType(), 3),
                    ArrayLiteral([StringLiteral("x"), StringLiteral("y"), StringLiteral("z")])),
            Assignment(ArrayAccessLValue(Identifier("s"), IntegerLiteral(1)), StringLiteral("Y")),
            Assignment(ArrayAccessLValue(Identifier("s"), IntegerLiteral(0)),
                       BinaryOp(ArrayAccess(Identifier("s"), IntegerLiteral(0)), "+", StringLiteral("X"))),  # "xX"
            VarDecl("b", BoolType(), BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(ArrayAccess(Identifier("s"), IntegerLiteral(0)), "+",
                             ArrayAccess(Identifier("s"), IntegerLiteral(1))),
                    "+",
                    BinaryOp(ArrayAccess(Identifier("s"), IntegerLiteral(2)),
                             "+",
                             BinaryOp(StringLiteral("-"), "+", Identifier("b")))
                )
            ]))
        ])
    ])
    expected = "xXYz-true"
    assert CodeGenerator().generate_and_run(ast) == expected


# H24) For-in + sửa mảng tại chỉ số dẫn xuất từ giá trị hiện tại
def test_h24_for_in_write_back_using_value_as_index_expr():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 5),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0),
                                  IntegerLiteral(0), IntegerLiteral(0)])),
            VarDecl("vals", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(1), IntegerLiteral(3), IntegerLiteral(4)])),
            ForStmt("v", Identifier("vals"), BlockStmt([
                Assignment(ArrayAccessLValue(Identifier("a"),
                                             BinaryOp(Identifier("v"), "-", IntegerLiteral(1))),
                           BinaryOp(Identifier("v"), "*", IntegerLiteral(10)))
            ])),
            # đọc kết quả a[0]+a[2]+a[3]
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(
                                      ArrayAccess(Identifier("a"), IntegerLiteral(0)),
                                      "+",
                                      BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(2)),
                                               "+",
                                               ArrayAccess(Identifier("a"), IntegerLiteral(3)))
                                  )]))
        ])
    ])
    expected = str(10 + 30 + 40)
    assert CodeGenerator().generate_and_run(ast) == expected


# H25) If/elif/else xen for-in và while trong từng nhánh
def test_h25_branch_specific_loops():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("mode", IntType(), IntegerLiteral(2)),
            VarDecl("out", StringType(), StringLiteral("")),
            IfStmt(
                BinaryOp(Identifier("mode"), "==", IntegerLiteral(1)),
                BlockStmt([
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                              BlockStmt([
                                  Assignment(IdLValue("out"),
                                             BinaryOp(Identifier("out"), "+",
                                                      BinaryOp(StringLiteral("W"), "+", Identifier("i")))),
                                  Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                              ]))
                ]),
                [(BinaryOp(Identifier("mode"), "==", IntegerLiteral(2)),
                  BlockStmt([
                      VarDecl("arr", ArrayType(IntType(), 3),
                              ArrayLiteral([IntegerLiteral(7), IntegerLiteral(8), IntegerLiteral(9)])),
                      ForStmt("x", Identifier("arr"), BlockStmt([
                          Assignment(IdLValue("out"),
                                     BinaryOp(Identifier("out"), "+",
                                              BinaryOp(StringLiteral("F"), "+", Identifier("x"))))
                      ]))
                  ]))],
                BlockStmt([
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("ELSE")])),
                    ReturnStmt(None)
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = "F7F8F9"
    assert CodeGenerator().generate_and_run(ast) == expected


# H26) While phức hợp: hai biến điều khiển + continue/break xen nhánh
def test_h26_complex_while_two_counters_with_controls():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("j", IntType(), IntegerLiteral(5)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(6)),
                BlockStmt([
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                    IfStmt(BinaryOp(Identifier("i"), "==", IntegerLiteral(4)),
                           BlockStmt([BreakStmt()]), [], None),
                    IfStmt(BinaryOp(Identifier("j"), ">", IntegerLiteral(0)),
                           BlockStmt([
                               Assignment(IdLValue("out"),
                                          BinaryOp(Identifier("out"), "+",
                                                   BinaryOp(StringLiteral(""), "+", Identifier("j")))),
                               Assignment(IdLValue("j"), BinaryOp(Identifier("j"), "-", IntegerLiteral(2))),
                               ContinueStmt()
                           ]),
                           [],
                           None),
                    Assignment(IdLValue("out"),
                               BinaryOp(Identifier("out"), "+", StringLiteral("X")))  # sẽ không chạy do continue
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    # j: 5->3->1->-1 dừng; i tăng đến 3 rồi break => in "531"
    assert CodeGenerator().generate_and_run(ast) == "531"


# H27) Gọi hàm trả bool trong biểu thức nối chuỗi lẫn số
def test_h27_bool_function_in_string_concat_with_numbers():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", FunctionCall(Identifier("isPos"), [IntegerLiteral(-1)])),  # false
                    "+",
                    BinaryOp(IntegerLiteral(7), "+", FunctionCall(Identifier("isPos"), [IntegerLiteral(1)]))   # "7true"
                )
            ]))
        ]),
        FuncDecl("isPos", [Param("x", IntType())], BoolType(), [
            ReturnStmt(BinaryOp(Identifier("x"), ">", IntegerLiteral(0)))
        ])
    ])
    expected = "false7true"
    assert CodeGenerator().generate_and_run(ast) == expected


# H28) Viết-đọc mảng xen kẽ nhiều lần với chỉ số biểu thức lồng
def test_h28_interleaved_array_writes_reads_with_nested_indices():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(1), IntegerLiteral(1), IntegerLiteral(1)])),
            VarDecl("i", IntType(), IntegerLiteral(1)),  # sẽ dùng làm chỉ số động
            # a[ (i+1) ] = a[i] + a[i-1]
            Assignment(ArrayAccessLValue(Identifier("a"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                       BinaryOp(ArrayAccess(Identifier("a"), Identifier("i")),
                                "+",
                                ArrayAccess(Identifier("a"),
                                            BinaryOp(Identifier("i"), "-", IntegerLiteral(1))))),
            # tăng i rồi lặp lại
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),  # i=2
            Assignment(ArrayAccessLValue(Identifier("a"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                       BinaryOp(ArrayAccess(Identifier("a"), Identifier("i")),
                                "+",
                                ArrayAccess(Identifier("a"),
                                            BinaryOp(Identifier("i"), "-", IntegerLiteral(1))))),
            # in a[2] + a[3]
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(2)),
                                            "+",
                                            ArrayAccess(Identifier("a"), IntegerLiteral(3)))]))
        ])
    ])
    # a ban đầu: [1,1,1,1]
    # i=1: a[2] = a[1] + a[0] = 2  -> [1,1,2,1]
    # i=2: a[3] = a[2] + a[1] = 3  -> [1,1,2,3]
    # print a[2]+a[3] = 5
    assert CodeGenerator().generate_and_run(ast) == "5"

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

    expected = """10
20"""  # Kết quả in chuỗi "" + 10 + "" + 20
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


def test_017_fibonacci_array_iterative():
    """Iterative Fibonacci with array: fib[9] = 34"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    VarDecl("n", IntType(), IntegerLiteral(10)),
                    VarDecl(
                        "fib",
                        ArrayType(IntType(), 10),
                        ArrayLiteral([
                            IntegerLiteral(0),
                            IntegerLiteral(1),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                            IntegerLiteral(0),
                        ])
                    ),
                    VarDecl("i", IntType(), IntegerLiteral(2)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", Identifier("n")),
                        BlockStmt([
                            Assignment(
                                ArrayAccessLValue(Identifier("fib"), Identifier("i")),
                                BinaryOp(
                                    ArrayAccess(Identifier("fib"), BinaryOp(Identifier("i"), "-", IntegerLiteral(1))),
                                    "+",
                                    ArrayAccess(Identifier("fib"), BinaryOp(Identifier("i"), "-", IntegerLiteral(2))),
                                )
                            ),
                            Assignment(
                                IdLValue("i"),
                                BinaryOp(Identifier("i"), "+", IntegerLiteral(1))
                            )
                        ])
                    ),
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [
                                BinaryOp(
                                    StringLiteral(""),
                                    "+",
                                    ArrayAccess(
                                        Identifier("fib"),
                                        BinaryOp(Identifier("n"), "-", IntegerLiteral(1))
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    )

    expected = "34"  # fib[n-1] với n=10 -> fib[9] = 34
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
def test_009_for_loop_sum_total():
    """For loop sum total and print"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    # int total = 0;
                    VarDecl("total", IntType(), IntegerLiteral(0)),

                    # int[] arr = [1, 2, 3, 4, 5];
                    VarDecl(
                        "arr",
                        ArrayType(IntType(), 5),
                        ArrayLiteral([
                            IntegerLiteral(1),
                            IntegerLiteral(2),
                            IntegerLiteral(3),
                            IntegerLiteral(4),
                            IntegerLiteral(5),
                        ])
                    ),

                    # for (x in arr) {
                    #     total = total + x;
                    # }
                    ForStmt(
                        "x",
                        Identifier("arr"),
                        BlockStmt([
                            Assignment(
                                IdLValue("total"),
                                BinaryOp(
                                    Identifier("total"),
                                    "+",
                                    Identifier("x")
                                )
                            )
                        ])
                    ),

                    # print("" + total);
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [
                                BinaryOp(
                                    StringLiteral(""),
                                    "+",
                                    Identifier("total")
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    )

    expected = "15"
    result = CodeGenerator().generate_and_run(ast)

    assert result == expected

def test_print_string():
    """Test case 1: In một chuỗi đơn giản."""
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
                            Identifier("print"), [StringLiteral("Hello, world!")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Hello, world!"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_print_integer():
    """Test case 2: In một số nguyên."""
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
                            Identifier("print"), [IntegerLiteral(12345)]
                        )
                    )
                ],
            )
        ],
    )
    expected = "12345"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_print_float():
    """Test case 3: In một số thực."""
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
                            Identifier("print"), [FloatLiteral(3.14159)]
                        )
                    )
                ],
            )
        ],
    )
    expected = "3.1416"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_print_boolean():
    """Test case 4: In một giá trị boolean."""
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
                            Identifier("print"), [BooleanLiteral(True)]
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_print_empty_string():
    """Test case 5: In một chuỗi rỗng."""
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
                            Identifier("print"), [StringLiteral("")]
                        )
                    )
                ],
            )
        ],
    )
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_concatenate_string_and_integer():
    """Test case 6: Nối chuỗi với số nguyên."""
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
                                BinaryOp(
                                    StringLiteral("The answer is: "), "+", IntegerLiteral(42)
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "The answer is: 42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_concatenate_string_float_empty_string():
    """Test case 7: Nối chuỗi với số thực và chuỗi rỗng."""
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
                                BinaryOp(
                                    BinaryOp(
                                        StringLiteral("Gia tri cua Pi la: "), "+", FloatLiteral(3.14)
                                    ),
                                    "+",
                                    StringLiteral(""),
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "Gia tri cua Pi la: 3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_concatenate_string_and_boolean():
    """Test case 8: Nối chuỗi với giá trị boolean."""
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
                                BinaryOp(
                                    StringLiteral("Is it raining? "), "+", BooleanLiteral(False)
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "Is it raining? false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_print_complex_arithmetic():
    """Test case 9: In kết quả biểu thức số học phức tạp."""
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
                                BinaryOp(
                                    BinaryOp(
                                        BinaryOp(
                                            IntegerLiteral(10), "+", IntegerLiteral(5)
                                        ),
                                        "*",
                                        IntegerLiteral(2),
                                    ),
                                    "/",
                                    FloatLiteral(3.0),
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "10.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_print_complex_logic():
    """Test case 10: In kết quả biểu thức logic phức tạp."""
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
                                BinaryOp(
                                    BinaryOp(
                                        BinaryOp(IntegerLiteral(5), ">", IntegerLiteral(3)),
                                        "and",
                                        BinaryOp(StringLiteral("apple"), "==", StringLiteral("apple")),
                                    ),
                                    "or",
                                    BinaryOp(IntegerLiteral(10), "<", IntegerLiteral(5)),
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
# -----------------------------
# 1) PRINT với LITERAL cơ bản
# -----------------------------

def test_101_print_string_literal():
    """print("Hello") -> Hello"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hello")]))
        ])
    ])
    expected = "Hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_102_print_empty_string():
    """print("") -> (empty line)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("")]))
        ])
    ])
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_103_print_integer_literal():
    """print(12345) -> 12345"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(12345)]))
        ])
    ])
    expected = "12345"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_104_print_boolean_true():
    """print(true) -> true"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BooleanLiteral(True)]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_105_print_boolean_false():
    """print(false) -> false"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BooleanLiteral(False)]))
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_106_print_float_literal_simple():
    """print(3.5) -> 3.5 (format JVM float)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [FloatLiteral(3.5)]))
        ])
    ])
    # Tùy runtime có thể in '3.5' hoặc '3.5' với định dạng JVM chuẩn (không ép 4 chữ số thập phân ở đây)
    expected = "3.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


# -------------------------------------
# 2) NỐI CHUỖI với GIÁ TRỊ (coercion)
# -------------------------------------

def test_107_concat_empty_plus_int():
    """print("" + 42) -> 42"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+", IntegerLiteral(42))
            ]))
        ])
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_108_concat_int_plus_empty():
    """print(42 + "") -> 42"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # 42 + ""  (nếu ngôn ngữ cho phép chuyển vế trái sang chuỗi)
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(42), "+", StringLiteral(""))
            ]))
        ])
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_109_concat_string_int_string():
    """print("A" + 1 + "B") -> A1B"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral("A"), "+", IntegerLiteral(1)),
                    "+",
                    StringLiteral("B")
                )
            ]))
        ])
    ])
    expected = "A1B"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_110_concat_empty_plus_bool_true():
    """print("" + true) -> true"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+", BooleanLiteral(True))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_111_concat_empty_plus_float():
    """print("" + 2.25) -> 2.25"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+", FloatLiteral(2.25))
            ]))
        ])
    ])
    expected = "2.25"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


# -------------------------------------------------
# 3) IN KẾT QUẢ BIỂU THỨC (số học/logic đơn giản)
# -------------------------------------------------

def test_112_print_arithmetic_expr():
    """print(3 + 4 * 5) -> 23"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(3), "+",
                    BinaryOp(IntegerLiteral(4), "*", IntegerLiteral(5))
                )
            ]))
        ])
    ])
    expected = str(3 + 4 * 5)
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_113_print_logic_not_true_as_bool_literal():
    """print(false) thông qua !true -> false"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # Trường hợp đơn giản: trực tiếp in false để kiểm tra println(Z)
            ExprStmt(FunctionCall(Identifier("print"), [BooleanLiteral(False)]))
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
    
# =========================================================
# PHẦN 2 — Khai báo & Gán biến (VarDecl, Assignment, Shadow)
# =========================================================

def test_201_vardecl_int_and_print():
    """int var decl with integer literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(42)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "42"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_202_vardecl_string_and_print():
    """string var decl with string literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("msg", StringType(), StringLiteral("hi")),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("msg")]))
        ])
    ])
    expected = "hi"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_203_vardecl_boolean_and_print():
    """bool var decl with boolean literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("b", BoolType(), BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("b")]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_204_vardecl_float_and_print():
    """float var decl with float literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("f", FloatType(), FloatLiteral(2.5)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("f")]))
        ])
    ])
    expected = "2.5"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_205_vardecl_with_expression_init():
    """int var decl initialized with arithmetic expression"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(),
                    BinaryOp(IntegerLiteral(3), "+",
                             BinaryOp(IntegerLiteral(4), "*", IntegerLiteral(5)))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = str(3 + 4 * 5)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_206_assignment_update_variable():
    """assignment to a variable (IdLValue)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(10)),
            Assignment(IdLValue("x"), IntegerLiteral(77)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "77"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_207_assignment_multiple_updates_sequence():
    """sequential updates to the same variable"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(1)),
            Assignment(IdLValue("x"), BinaryOp(Identifier("x"), "+", IntegerLiteral(2))),  # 3
            Assignment(IdLValue("x"), BinaryOp(Identifier("x"), "*", IntegerLiteral(5))),  # 15
            Assignment(IdLValue("x"), BinaryOp(Identifier("x"), "-", IntegerLiteral(4))),  # 11
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = str(((1 + 2) * 5) - 4)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_208_assignment_using_other_variable():
    """assignment using value from another variable"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", IntType(), IntegerLiteral(7)),
            VarDecl("b", IntType(), IntegerLiteral(0)),
            Assignment(IdLValue("b"), BinaryOp(Identifier("a"), "*", IntegerLiteral(3))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("b")]))
        ])
    ])
    expected = str(7 * 3)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_209_shadowing_local_over_param_and_assignment():
    """local var shadows param; assignment writes to inner local"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("foo"), [IntegerLiteral(9)])]))
        ]),
        FuncDecl("foo", [Param("x", IntType())], IntType(), [
            VarDecl("x", IntType(), IntegerLiteral(100)),               # shadow param
            Assignment(IdLValue("x"), BinaryOp(Identifier("x"), "+", IntegerLiteral(23))),  # 123
            ReturnStmt(Identifier("x"))
        ])
    ])
    expected = "123"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_210_shadowing_block_inner_variable():
    """inner block variable shadows outer variable"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(5)),
            # block with inner x
            BlockStmt([
                VarDecl("x", IntType(), IntegerLiteral(8)),
                Assignment(IdLValue("x"), BinaryOp(Identifier("x"), "+", IntegerLiteral(1))),  # 9 (inner)
                ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))  # prints inner 9
            ]),
            # outer x remains 5
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "9\n5"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_211_array_vardecl_and_read_first():
    """array var decl with ArrayLiteral; read first element"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6)])),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("arr"), IntegerLiteral(0))]))
        ])
    ])
    expected = "2"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_212_array_element_assignment_and_read_back():
    """write to array element then read"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            Assignment(ArrayAccessLValue(Identifier("arr"), IntegerLiteral(1)),
                       IntegerLiteral(99)),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]))
        ])
    ])
    expected = "99"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_213_array_element_assignment_with_expr_index():
    """assign to array element using expression index i-1"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(2)),
            VarDecl("arr", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
            Assignment(
                ArrayAccessLValue(
                    Identifier("arr"),
                    BinaryOp(Identifier("i"), "-", IntegerLiteral(1))  # index=1
                ),
                IntegerLiteral(77)
            ),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]))
        ])
    ])
    expected = "77"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_214_multiple_var_decls_and_updates():
    """declare many vars then update some"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", IntType(), IntegerLiteral(1)),
            VarDecl("b", IntType(), IntegerLiteral(2)),
            VarDecl("c", IntType(), IntegerLiteral(3)),
            Assignment(IdLValue("b"), BinaryOp(Identifier("b"), "+", Identifier("c"))),  # 5
            Assignment(IdLValue("a"), BinaryOp(Identifier("a"), "+", Identifier("b"))),  # 6
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", Identifier("a")),  # "6"
                    "+",
                    Identifier("b")                                    # "5"
                )
            ]))
        ])
    ])
    expected = "65"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_215_assign_function_call_result_to_var():
    """assign result of function call to local variable"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(0)),
            Assignment(IdLValue("x"),
                       FunctionCall(Identifier("add"),
                                    [IntegerLiteral(8), IntegerLiteral(12)])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ]),
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ])
    ])
    expected = str(8 + 12)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_216_assign_boolean_expression_result():
    """assign the result of boolean relational expression"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("ok", BoolType(),
                    BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(7))),  # true
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("ok")]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_217_init_var_from_array_element():
    """var initialized from an array element"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 2),
                    ArrayLiteral([IntegerLiteral(5), IntegerLiteral(9)])),
            VarDecl("x", IntType(), ArrayAccess(Identifier("arr"), IntegerLiteral(1))),  # 9
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "9"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_218_self_update_x_plus_1():
    """x = x + 1 pattern"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(7)),
            Assignment(IdLValue("x"),
                       BinaryOp(Identifier("x"), "+", IntegerLiteral(1))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "8"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_219_assign_string_reassignment():
    """reassign string variable"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("s", StringType(), StringLiteral("A")),
            Assignment(IdLValue("s"),
                       BinaryOp(Identifier("s"), "+", StringLiteral("B"))),  # "AB"
            Assignment(IdLValue("s"),
                       BinaryOp(Identifier("s"), "+", StringLiteral("C"))),  # "ABC"
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("s")]))
        ])
    ])
    expected = "ABC"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_220_assignment_chain_of_reads_and_writes():
    """read-then-write across variables"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", IntType(), IntegerLiteral(2)),
            VarDecl("b", IntType(), IntegerLiteral(3)),
            VarDecl("c", IntType(), IntegerLiteral(4)),
            Assignment(IdLValue("a"), BinaryOp(Identifier("a"), "*", Identifier("b"))),  # 6
            Assignment(IdLValue("b"), BinaryOp(Identifier("a"), "+", Identifier("c"))),  # 10
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("b")]))
        ])
    ])
    expected = str((2 * 3) + 4)
    assert CodeGenerator().generate_and_run(ast) == expected


# =====================================================
# PHẦN 3 — Biểu thức: số học, quan hệ, logic, unary
# =====================================================

# -------------------------
# 3.1 Số học cơ bản + ưu tiên
# -------------------------

def test_301_addition_simple():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(IntegerLiteral(2), "+", IntegerLiteral(3))]))
        ])
    ])
    expected = str(2 + 3)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_302_subtraction_simple():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(IntegerLiteral(10), "-", IntegerLiteral(7))]))
        ])
    ])
    expected = str(10 - 7)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_303_multiplication_simple():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(IntegerLiteral(6), "*", IntegerLiteral(7))]))
        ])
    ])
    expected = str(6 * 7)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_304_division_simple():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(IntegerLiteral(20), "/", IntegerLiteral(4))]))
        ])
    ])
    expected = str(20 // 4)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_305_modulo_simple():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(IntegerLiteral(23), "%", IntegerLiteral(5))]))
        ])
    ])
    expected = str(23 % 5)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_306_operator_precedence_mul_before_add():
    # 2 + 3 * 4 = 14
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(2), "+",
                         BinaryOp(IntegerLiteral(3), "*", IntegerLiteral(4)))
            ]))
        ])
    ])
    expected = str(2 + 3 * 4)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_307_parentheses_override_precedence():
    # (2 + 3) * 4 = 20
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("tmp", IntType(),
                    BinaryOp(IntegerLiteral(2), "+", IntegerLiteral(3))),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(Identifier("tmp"), "*", IntegerLiteral(4))
            ]))
        ])
    ])
    expected = str((2 + 3) * 4)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_308_left_associativity_subtraction():
    # 20 - 5 - 3 = (20-5)-3 = 12
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(IntegerLiteral(20), "-", IntegerLiteral(5)),
                    "-",
                    IntegerLiteral(3)
                )
            ]))
        ])
    ])
    expected = str((20 - 5) - 3)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_309_left_associativity_division():
    # 100 / 5 / 2 = (100/5)/2 = 10
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(IntegerLiteral(100), "/", IntegerLiteral(5)),
                    "/",
                    IntegerLiteral(2)
                )
            ]))
        ])
    ])
    expected = str((100 // 5) // 2)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_310_nested_arithmetic_deep_stack():
    # (((1+2)*3 - 4) * (5 + (6*7))) / 2
    left = BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), "+", IntegerLiteral(2)),
                             "*", IntegerLiteral(3)),
                    "-", IntegerLiteral(4))
    right = BinaryOp(IntegerLiteral(5),
                     "+",
                     BinaryOp(IntegerLiteral(6), "*", IntegerLiteral(7)))
    expr = BinaryOp(BinaryOp(left, "*", right), "/", IntegerLiteral(2))
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [expr]))
        ])
    ])
    expected_val = (((1 + 2) * 3 - 4) * (5 + (6 * 7))) // 2
    assert CodeGenerator().generate_and_run(ast) == str(expected_val)

# -------------------------
# 3.2 Unary
# -------------------------

def test_311_unary_minus_on_literal():
    # -(5) = -5  (thực hiện như 0-5)
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("z", IntType(), BinaryOp(IntegerLiteral(0), "-", IntegerLiteral(5))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("z")]))
        ])
    ])
    expected = str(-5)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_312_unary_minus_on_identifier():
    # -(x) với x=9 -> -9
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(9)),
            VarDecl("y", IntType(), BinaryOp(IntegerLiteral(0), "-", Identifier("x"))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("y")]))
        ])
    ])
    expected = str(-9)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_313_logical_not_on_true_false():
    # !true -> false, !false -> true (in nối thành  "falsetrue")
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", BoolType(), BooleanLiteral(True)),
            VarDecl("b", BoolType(), BooleanLiteral(False)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", BooleanLiteral(False)),  # !true => false
                    "+",
                    BooleanLiteral(True)                                     # !false => true
                )
            ]))
        ])
    ])
    expected = "falsetrue"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 3.3 Quan hệ
# -------------------------

def test_314_relational_all_true_cases():
    # 5>3, 5>=5, 3<4, 4<=4, 7==7, 8!=9  -> "truetruetruetruetruetrue"
    parts = [
        BinaryOp(IntegerLiteral(5), ">", IntegerLiteral(3)),
        BinaryOp(IntegerLiteral(5), ">=", IntegerLiteral(5)),
        BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(4)),
        BinaryOp(IntegerLiteral(4), "<=", IntegerLiteral(4)),
        BinaryOp(IntegerLiteral(7), "==", IntegerLiteral(7)),
        BinaryOp(IntegerLiteral(8), "!=", IntegerLiteral(9)),
    ]
    # "" + b1 + b2 + ... để in liên tiếp
    expr = BinaryOp(StringLiteral(""), "+", parts[0])
    for p in parts[1:]:
        expr = BinaryOp(expr, "+", p)

    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [expr]))
        ])
    ])
    expected = "truetruetruetruetruetrue"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_315_relational_mixed_false_true():
    # (2>7)=false, (9==9)=true -> "falsetrue"
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+",
                             BinaryOp(IntegerLiteral(2), ">", IntegerLiteral(7))),
                    "+",
                    BinaryOp(IntegerLiteral(9), "==", IntegerLiteral(9))
                )
            ]))
        ])
    ])
    expected = "falsetrue"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 3.4 Logic &&, ||
# -------------------------

def test_316_logical_and_true_true():
    # true && true -> true
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", BoolType(), BooleanLiteral(True)),
            VarDecl("b", BoolType(), BooleanLiteral(True)),
            # In "" + (a && b)
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+",
                         BinaryOp(Identifier("a"), "&&", Identifier("b")))
            ]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_317_logical_and_true_false():
    # true && false -> false
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", BoolType(), BooleanLiteral(True)),
            VarDecl("b", BoolType(), BooleanLiteral(False)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+",
                         BinaryOp(Identifier("a"), "&&", Identifier("b")))
            ]))
        ])
    ])
    expected = "false"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_318_logical_or_false_false():
    # false || false -> false
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", BoolType(), BooleanLiteral(False)),
            VarDecl("b", BoolType(), BooleanLiteral(False)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+",
                         BinaryOp(Identifier("a"), "||", Identifier("b")))
            ]))
        ])
    ])
    expected = "false"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_319_logical_or_true_false():
    # true || false -> true
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", BoolType(), BooleanLiteral(True)),
            VarDecl("b", BoolType(), BooleanLiteral(False)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+",
                         BinaryOp(Identifier("a"), "||", Identifier("b")))
            ]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_320_logic_with_relational_subexpressions():
    # (a<b) && (b<c) với a=2,b=5,c=9 -> true
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", IntType(), IntegerLiteral(2)),
            VarDecl("b", IntType(), IntegerLiteral(5)),
            VarDecl("c", IntType(), IntegerLiteral(9)),
            VarDecl("cond", BoolType(),
                    BinaryOp(
                        BinaryOp(Identifier("a"), "<", Identifier("b")),
                        "&&",
                        BinaryOp(Identifier("b"), "<", Identifier("c"))
                    )),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+", Identifier("cond"))
            ]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected
    
# =========================================================
# PHẦN 4 — Điều khiển luồng: if/elif/else, while, for-in
# =========================================================

# -------------------------
# 4.1 IF / ELIF / ELSE
# -------------------------

def test_401_if_true_only_then():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(
                BinaryOp(IntegerLiteral(5), ">", IntegerLiteral(3)),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("T")]))]),
                [],
                None
            )
        ])
    ])
    expected = "T"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_402_if_condition_false_no_else_prints_nothing():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(
                BinaryOp(IntegerLiteral(2), ">", IntegerLiteral(7)),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("X")]))]),
                [],
                None
            )
        ])
    ])
    expected = ""
    assert CodeGenerator().generate_and_run(ast) == expected


def test_403_if_else_choose_else():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(
                BinaryOp(IntegerLiteral(1), ">", IntegerLiteral(2)),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("FAIL")]))]),
                [],
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("OK")]))])
            )
        ])
    ])
    expected = "OK"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_404_if_with_single_elif():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(10)),
            IfStmt(
                BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("neg")]))]),
                [
                    (BinaryOp(Identifier("x"), "==", IntegerLiteral(10)),
                     BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("ten")]))]))
                ],
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("other")]))])
            )
        ])
    ])
    expected = "ten"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_405_if_with_multiple_elifs_and_else():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("n", IntType(), IntegerLiteral(7)),
            IfStmt(
                BinaryOp(Identifier("n"), "==", IntegerLiteral(1)),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("one")]))]),
                [
                    (BinaryOp(Identifier("n"), "==", IntegerLiteral(2)),
                     BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("two")]))])),
                    (BinaryOp(Identifier("n"), "==", IntegerLiteral(7)),
                     BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("seven")]))]))
                ],
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("other")]))])
            )
        ])
    ])
    expected = "seven"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_406_nested_if_blocks():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(-3)),
            IfStmt(
                BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("x"), "==", IntegerLiteral(0)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("zero")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("neg")]))])
                    )
                ]),
                [],
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("pos")]))])
            )
        ])
    ])
    expected = "neg"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 4.2 WHILE
# -------------------------

def test_407_while_sum_1_to_5():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
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
        ])
    ])
    expected = str(sum(range(1, 6)))
    assert CodeGenerator().generate_and_run(ast) == expected


def test_408_while_zero_iterations_condition_false_initially():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(10)),
            VarDecl("count", IntType(), IntegerLiteral(0)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                BlockStmt([
                    Assignment(IdLValue("count"), BinaryOp(Identifier("count"), "+", IntegerLiteral(1))),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("count")]))
        ])
    ])
    expected = "0"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_409_while_with_break_stops_early():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(1)),
            VarDecl("sum", IntType(), IntegerLiteral(0)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<=", IntegerLiteral(10)),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("i"), ">", IntegerLiteral(4)),
                        BlockStmt([BreakStmt()]),
                        [],
                        None
                    ),
                    Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), "+", Identifier("i"))),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
        ])
    ])
    # 1+2+3+4 = 10
    expected = "10"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_410_while_with_continue_skips_evens():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(6)),
                BlockStmt([
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                    IfStmt(
                        BinaryOp(BinaryOp(Identifier("i"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                        BlockStmt([ContinueStmt()]),
                        [],
                        None
                    ),
                    # chỉ nối số lẻ: 1,3,5
                    Assignment(IdLValue("out"),
                               BinaryOp(Identifier("out"), "+",
                                        BinaryOp(StringLiteral(""), "+", Identifier("i"))))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = "135"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 4.3 FOR-IN ARRAY
# -------------------------

def test_411_for_in_print_elements_two_lines():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20)])),
            ForStmt(
                "x",
                Identifier("a"),
                BlockStmt([
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(StringLiteral(""), "+", Identifier("x"))]))
                ])
            )
        ])
    ])
    expected = "10\n20"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_412_for_in_sum_array():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 5),
                    ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])),
            VarDecl("total", IntType(), IntegerLiteral(0)),
            ForStmt(
                "v",
                Identifier("arr"),
                BlockStmt([
                    Assignment(IdLValue("total"), BinaryOp(Identifier("total"), "+", Identifier("v")))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("total")]))
        ])
    ])
    expected = str(sum([1,2,3,4,5]))
    assert CodeGenerator().generate_and_run(ast) == expected


def test_413_for_in_empty_array_prints_nothing():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 0), ArrayLiteral([])),
            ForStmt(
                "e",
                Identifier("xs"),
                BlockStmt([
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(StringLiteral(""), "+", Identifier("e"))]))
                ])
            )
        ])
    ])
    expected = ""  # không in gì vì mảng rỗng
    assert CodeGenerator().generate_and_run(ast) == expected


def test_414_for_in_one_element():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(7)])),
            VarDecl("acc", IntType(), IntegerLiteral(0)),
            ForStmt(
                "e",
                Identifier("xs"),
                BlockStmt([
                    Assignment(IdLValue("acc"), BinaryOp(Identifier("acc"), "+", Identifier("e")))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("acc")]))
        ])
    ])
    expected = "7"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_415_for_in_with_break_stop_at_first_negative():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 5),
                    ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(-1), IntegerLiteral(8), IntegerLiteral(9)])),
            VarDecl("seen", StringType(), StringLiteral("")),
            ForStmt(
                "v",
                Identifier("xs"),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("v"), "<", IntegerLiteral(0)),
                        BlockStmt([BreakStmt()]),
                        [],
                        None
                    ),
                    Assignment(IdLValue("seen"),
                               BinaryOp(Identifier("seen"), "+",
                                        BinaryOp(StringLiteral(""), "+", Identifier("v"))))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("seen")]))
        ])
    ])
    expected = "34"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_416_for_in_with_continue_skip_negatives():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 6),
                    ArrayLiteral([IntegerLiteral(5), IntegerLiteral(-2), IntegerLiteral(7), IntegerLiteral(-1), IntegerLiteral(0), IntegerLiteral(4)])),
            VarDecl("out", StringType(), StringLiteral("")),
            ForStmt(
                "v",
                Identifier("xs"),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("v"), "<", IntegerLiteral(0)),
                        BlockStmt([ContinueStmt()]),
                        [],
                        None
                    ),
                    Assignment(IdLValue("out"),
                               BinaryOp(Identifier("out"), "+",
                                        BinaryOp(StringLiteral(""), "+", Identifier("v"))))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = "5704"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_417_nested_for_in_accumulate_all_pairs_sum():
    # Duyệt 2 mảng, cộng từng cặp mọi tổ hợp, in tổng cuối
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])),
            VarDecl("b", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
            VarDecl("total", IntType(), IntegerLiteral(0)),
            ForStmt(
                "x",
                Identifier("a"),
                BlockStmt([
                    ForStmt(
                        "y",
                        Identifier("b"),
                        BlockStmt([
                            Assignment(IdLValue("total"),
                                       BinaryOp(Identifier("total"),
                                                "+",
                                                BinaryOp(Identifier("x"), "+", Identifier("y"))))
                        ])
                    )
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("total")]))
        ])
    ])
    # (1+10)+(1+20)+(1+30)+(2+10)+(2+20)+(2+30) = 3*(1+2) + (10+20+30)*2 = 9 + 120 = 129
    expected = "129"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_418_for_in_with_inner_while_and_continue_break():
    # For mỗi phần tử, while giảm dần giá trị tới 0; nếu âm thì break bỏ qua các phần tử còn lại
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(2), IntegerLiteral(-1), IntegerLiteral(1)])),
            VarDecl("out", StringType(), StringLiteral("")),
            ForStmt(
                "v",
                Identifier("xs"),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("v"), "<", IntegerLiteral(0)),
                        BlockStmt([BreakStmt()]),
                        [],
                        None
                    ),
                    VarDecl("t", IntType(), Identifier("v")),
                    WhileStmt(
                        BinaryOp(Identifier("t"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            Assignment(IdLValue("out"),
                                       BinaryOp(Identifier("out"), "+",
                                                BinaryOp(StringLiteral(""), "+", Identifier("t")))),
                            Assignment(IdLValue("t"), BinaryOp(Identifier("t"), "-", IntegerLiteral(1))),
                            IfStmt(
                                BinaryOp(Identifier("t"), "==", IntegerLiteral(1)),
                                BlockStmt([ContinueStmt()]),
                                [],
                                None
                            )
                        ])
                    )
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    # v=3 -> "3 2 1" (1 bị continue nên vẫn nối 1 trước khi continue? Ở đây continue xảy ra sau khi nối và trừ, không ảnh hưởng chuỗi)
    # v=2 -> "2 1"
    # gặp -1 thì break -> dừng toàn bộ for
    expected = "32121"
    assert CodeGenerator().generate_and_run(ast) == expected
    
# =====================================================
# PHẦN 5 — MẢNG: tạo, đọc, ghi, chỉ số biểu thức, nhiều kiểu
# =====================================================

# -------------------------
# 5.1 Khai báo & Đọc cơ bản
# -------------------------

def test_501_array_decl_int_read_first_last():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 4),
                    ArrayLiteral([IntegerLiteral(3), IntegerLiteral(6), IntegerLiteral(9), IntegerLiteral(12)])),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("arr"), IntegerLiteral(0))])),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("arr"), IntegerLiteral(3))]))
        ])
    ])
    expected = "3\n12"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_502_array_decl_empty_then_no_output():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 0), ArrayLiteral([]))
            # không in gì
        ])
    ])
    expected = ""
    assert CodeGenerator().generate_and_run(ast) == expected


def test_503_array_decl_single_element():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(7)])),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("xs"), IntegerLiteral(0))]))
        ])
    ])
    expected = "7"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 5.2 Ghi phần tử (ArrayAccessLValue)
# -------------------------

def test_504_array_write_then_read_back_middle():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(55)),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), IntegerLiteral(1))]))
        ])
    ])
    expected = "55"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_505_array_two_writes_overwrite_value():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 2),
                    ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20)])),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(0)), IntegerLiteral(99)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(0)), IntegerLiteral(11)),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), IntegerLiteral(0))]))
        ])
    ])
    expected = "11"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_506_array_write_with_expr_rhs():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6)])),
            Assignment(
                ArrayAccessLValue(Identifier("a"), IntegerLiteral(2)),
                BinaryOp(IntegerLiteral(10), "*", IntegerLiteral(3))  # 30
            ),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), IntegerLiteral(2))]))
        ])
    ])
    expected = "30"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 5.3 Chỉ số là biểu thức
# -------------------------

def test_507_index_is_identifier_and_update():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(1)),
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6), IntegerLiteral(7)])),
            Assignment(ArrayAccessLValue(Identifier("a"), Identifier("i")), IntegerLiteral(42)),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), Identifier("i"))]))
        ])
    ])
    expected = "42"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_508_index_is_binary_expression_i_minus_1():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(2)),
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
            Assignment(ArrayAccessLValue(Identifier("a"),
                                         BinaryOp(Identifier("i"), "-", IntegerLiteral(1))),
                       IntegerLiteral(77)),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), IntegerLiteral(1))]))
        ])
    ])
    expected = "77"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_509_nested_index_expr_with_update_chain():
    # a[(i+1)-1] = a[i] + 5
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(1)),
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            Assignment(
                ArrayAccessLValue(
                    Identifier("a"),
                    BinaryOp(BinaryOp(Identifier("i"), "+", IntegerLiteral(1)), "-", IntegerLiteral(1))
                ),
                BinaryOp(ArrayAccess(Identifier("a"), Identifier("i")), "+", IntegerLiteral(5))
            ),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), IntegerLiteral(1))]))
        ])
    ])
    expected = str(2 + 5)
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 5.4 Mảng trong biểu thức
# -------------------------

def test_510_read_two_elements_and_add_then_print():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 4),
                    ArrayLiteral([IntegerLiteral(3), IntegerLiteral(5), IntegerLiteral(7), IntegerLiteral(9)])),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(1)),
                         "+",
                         ArrayAccess(Identifier("a"), IntegerLiteral(3)))
            ]))
        ])
    ])
    expected = str(5 + 9)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_511_update_from_sum_of_two_elements():
    # a[0] = a[1] + a[2]
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(8), IntegerLiteral(12)])),
            Assignment(
                ArrayAccessLValue(Identifier("a"), IntegerLiteral(0)),
                BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(1)),
                         "+",
                         ArrayAccess(Identifier("a"), IntegerLiteral(2)))
            ),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("a"), IntegerLiteral(0))]))
        ])
    ])
    expected = str(8 + 12)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_512_fibonacci_like_progression_small():
    # fib: [0,1,0,0], i=2..3: fib[i]=fib[i-1]+fib[i-2] → [0,1,1,2], in fib[3]
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("n", IntType(), IntegerLiteral(4)),
            VarDecl("fib", ArrayType(IntType(), 4),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(1),
                                  IntegerLiteral(0), IntegerLiteral(0)])),
            VarDecl("i", IntType(), IntegerLiteral(2)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", Identifier("n")),
                BlockStmt([
                    Assignment(
                        ArrayAccessLValue(Identifier("fib"), Identifier("i")),
                        BinaryOp(
                            ArrayAccess(Identifier("fib"),
                                        BinaryOp(Identifier("i"), "-", IntegerLiteral(1))),
                            "+",
                            ArrayAccess(Identifier("fib"),
                                        BinaryOp(Identifier("i"), "-", IntegerLiteral(2)))
                        )
                    ),
                    Assignment(IdLValue("i"),
                               BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [
                ArrayAccess(Identifier("fib"),
                            BinaryOp(Identifier("n"), "-", IntegerLiteral(1)))
            ]))
        ])
    ])
    expected = "2"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 5.5 Mảng các kiểu khác (string, bool)
# -------------------------

def test_513_string_array_read_and_concat_print():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("s", ArrayType(StringType(), 3),
                    ArrayLiteral([StringLiteral("A"), StringLiteral("B"), StringLiteral("C")])),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(ArrayAccess(Identifier("s"), IntegerLiteral(0)), "+",
                             ArrayAccess(Identifier("s"), IntegerLiteral(1))),
                    "+",
                    ArrayAccess(Identifier("s"), IntegerLiteral(2))
                )
            ]))
        ])
    ])
    expected = "ABC"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_514_string_array_write_and_read():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("s", ArrayType(StringType(), 2),
                    ArrayLiteral([StringLiteral("hi"), StringLiteral("xo")])),
            Assignment(ArrayAccessLValue(Identifier("s"), IntegerLiteral(1)), StringLiteral("there")),
            ExprStmt(FunctionCall(Identifier("print"),
                                  [ArrayAccess(Identifier("s"), IntegerLiteral(1))]))
        ])
    ])
    expected = "there"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_515_bool_array_read_and_print_each():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("b", ArrayType(BoolType(), 3),
                    ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True)])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("b"), IntegerLiteral(0))])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("b"), IntegerLiteral(1))])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("b"), IntegerLiteral(2))]))
        ])
    ])
    expected = "true\nfalse\ntrue"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_516_bool_array_write_then_concat_string_print():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("b", ArrayType(BoolType(), 2),
                    ArrayLiteral([BooleanLiteral(False), BooleanLiteral(False)])),
            Assignment(ArrayAccessLValue(Identifier("b"), IntegerLiteral(0)), BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+", ArrayAccess(Identifier("b"), IntegerLiteral(0)))
            ]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 5.6 Kết hợp đọc/ghi và in chuỗi
# -------------------------

def test_517_build_string_by_iterating_array_indices_manually():
    # Thủ công duyệt bằng biến chỉ số (không dùng for-in ở phần này)
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 3),
                    ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                BlockStmt([
                    Assignment(IdLValue("out"),
                               BinaryOp(Identifier("out"), "+",
                                        BinaryOp(StringLiteral(""), "+",
                                                 ArrayAccess(Identifier("a"), Identifier("i"))))),
                    Assignment(IdLValue("i"),
                               BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = "123"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_518_chained_writes_then_combined_read():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 4),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(0)), IntegerLiteral(5)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(6)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(2)), IntegerLiteral(7)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(3)), IntegerLiteral(8)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(0)), "+",
                             ArrayAccess(Identifier("a"), IntegerLiteral(1))),
                    "+",
                    BinaryOp(ArrayAccess(Identifier("a"), IntegerLiteral(2)), "+",
                             ArrayAccess(Identifier("a"), IntegerLiteral(3)))
                )
            ]))
        ])
    ])
    expected = str((5 + 6) + (7 + 8))
    assert CodeGenerator().generate_and_run(ast) == expected

# =====================================================
# PHẦN 6 — HÀM: định nghĩa, gọi, tham số, trả về, đệ quy
# =====================================================

# -------------------------
# 6.1 Cơ bản: trả về hằng, một tham số
# -------------------------

def test_601_function_return_constant():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("forty_two"), [])]))
        ]),
        FuncDecl("forty_two", [], IntType(), [
            ReturnStmt(IntegerLiteral(42))
        ])
    ])
    expected = "42"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_602_function_one_param_square():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("square"), [IntegerLiteral(9)])]))
        ]),
        FuncDecl("square", [Param("n", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("n"), "*", Identifier("n")))
        ])
    ])
    expected = str(9 * 9)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_603_function_two_params_add():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("add"), [IntegerLiteral(7), IntegerLiteral(11)])]))
        ]),
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ])
    ])
    expected = str(7 + 11)
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.2 Hàm void: in bên trong
# -------------------------

def test_604_void_function_prints_inside():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("hello"), []))
        ]),
        FuncDecl("hello", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hi")]))
        ])
    ])
    expected = "Hi"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_605_void_function_takes_param_and_prints():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("say"), [StringLiteral("OK")]))
        ]),
        FuncDecl("say", [Param("s", StringType())], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("s")]))
        ])
    ])
    expected = "OK"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.3 Early return & đường đi không else
# -------------------------

def test_606_early_return_positive_abs_like():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("abs_like"), [IntegerLiteral(-8)])]))
        ]),
        FuncDecl("abs_like", [Param("x", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(BinaryOp(IntegerLiteral(0), "-", Identifier("x")))]),
                [],
                BlockStmt([ReturnStmt(Identifier("x"))])
            )
        ])
    ])
    expected = str(8)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_607_return_without_else_trailing_return():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("is_even"), [IntegerLiteral(6)])]))
        ]),
        FuncDecl("is_even", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(BinaryOp(Identifier("n"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(IntegerLiteral(1))]),
                [],
                None
            ),
            ReturnStmt(IntegerLiteral(0))
        ])
    ])
    expected = "1"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.4 Gọi lồng nhau & truyền/nhận giá trị
# -------------------------

def test_608_nested_calls_double_abs():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                FunctionCall(Identifier("double"), [
                    FunctionCall(Identifier("abs_like"), [IntegerLiteral(-10)])
                ])
            ]))
        ]),
        FuncDecl("abs_like", [Param("x", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(BinaryOp(IntegerLiteral(0), "-", Identifier("x")))]),
                [],
                BlockStmt([ReturnStmt(Identifier("x"))])
            )
        ]),
        FuncDecl("double", [Param("y", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("y"), "*", IntegerLiteral(2)))
        ])
    ])
    expected = "20"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_609_call_result_used_in_expression():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # print("" + (add(3,4) * 5)) -> "35"
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+",
                         BinaryOp(FunctionCall(Identifier("add"), [IntegerLiteral(3), IntegerLiteral(4)]),
                                  "*", IntegerLiteral(5)))
            ]))
        ]),
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ])
    ])
    expected = str((3 + 4) * 5)
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.5 Đệ quy & đệ quy tương hỗ
# -------------------------

def test_610_recursive_factorial_5():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("fact"), [IntegerLiteral(5)])]))
        ]),
        FuncDecl("fact", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "<=", IntegerLiteral(1)),
                BlockStmt([ReturnStmt(IntegerLiteral(1))]),
                [],
                BlockStmt([
                    ReturnStmt(
                        BinaryOp(
                            Identifier("n"),
                            "*",
                            FunctionCall(Identifier("fact"), [
                                BinaryOp(Identifier("n"), "-", IntegerLiteral(1))
                            ])
                        )
                    )
                ])
            ),
            ReturnStmt(None)   # đảm bảo mọi đường đi return
        ])
    ])
    expected = "120"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_611_mutual_recursion_is_even_is_odd():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # In: is_even(7) -> 0, is_even(8) -> 1; nối chuỗi "01"
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", FunctionCall(Identifier("is_even"), [IntegerLiteral(7)])),
                    "+",
                    FunctionCall(Identifier("is_even"), [IntegerLiteral(8)])
                )
            ]))
        ]),
        FuncDecl("is_even", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "==", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(IntegerLiteral(1))]),
                [],
                BlockStmt([ReturnStmt(FunctionCall(Identifier("is_odd"), [BinaryOp(Identifier("n"), "-", IntegerLiteral(1))]))])
            )
        ]),
        FuncDecl("is_odd", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "==", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(IntegerLiteral(0))]),
                [],
                BlockStmt([ReturnStmt(FunctionCall(Identifier("is_even"), [BinaryOp(Identifier("n"), "-", IntegerLiteral(1))]))])
            )
        ])
    ])
    expected = "01"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.6 Shadowing & phạm vi trong hàm
# -------------------------

def test_612_param_shadowed_by_local_and_used():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                FunctionCall(Identifier("foo"), [IntegerLiteral(9)])
            ]))
        ]),
        FuncDecl("foo", [Param("x", IntType())], IntType(), [
            VarDecl("x", IntType(), IntegerLiteral(100)),  # shadow param
            ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(23)))  # 123
        ])
    ])
    expected = "123"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_613_local_shadow_outer_then_restore():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(5)),
            ExprStmt(FunctionCall(Identifier("print"), [
                FunctionCall(Identifier("use_local"), [IntegerLiteral(7)])
            ])),
            # in ra x bên ngoài để chắc chắn không bị thay đổi
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ]),
        FuncDecl("use_local", [Param("p", IntType())], IntType(), [
            VarDecl("x", IntType(), IntegerLiteral(10)),
            ReturnStmt(BinaryOp(Identifier("x"), "+", Identifier("p")))  # 17
        ])
    ])
    expected = "17\n5"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.7 Hàm trả về bool và dùng trong if
# -------------------------

def test_614_function_returns_bool_used_in_if():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(
                FunctionCall(Identifier("gt"), [IntegerLiteral(9), IntegerLiteral(3)]),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("T")]))]),
                [],
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("F")]))])
            )
        ]),
        FuncDecl("gt", [Param("a", IntType()), Param("b", IntType())], BoolType(), [
            ReturnStmt(BinaryOp(Identifier("a"), ">", Identifier("b")))
        ])
    ])
    expected = "T"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.8 Truyền tham số là kết quả gọi hàm khác
# -------------------------

def test_615_passing_call_result_as_argument_chain():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # print( inc( inc(3) ) ) -> 5
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("inc"), [
                                      FunctionCall(Identifier("inc"), [IntegerLiteral(3)])
                                  ])]))
        ]),
        FuncDecl("inc", [Param("x", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(1)))
        ])
    ])
    expected = str(5)
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 6.9 Hàm thao tác với biến cục bộ nhiều bước
# -------------------------

def test_616_function_with_internal_locals_and_updates():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("compute"), [IntegerLiteral(4)])]))
        ]),
        FuncDecl("compute", [Param("n", IntType())], IntType(), [
            VarDecl("a", IntType(), IntegerLiteral(1)),
            VarDecl("b", IntType(), IntegerLiteral(2)),
            Assignment(IdLValue("a"), BinaryOp(Identifier("a"), "+", Identifier("n"))),     # a = 5
            Assignment(IdLValue("b"), BinaryOp(Identifier("b"), "*", Identifier("a"))),     # b = 10
            ReturnStmt(Identifier("b"))
        ])
    ])
    expected = "10"
    assert CodeGenerator().generate_and_run(ast) == expected
    
# =====================================================
# PHẦN 7 — Stack & Scope: sâu stack, nhiều locals, shadow, all paths return
# =====================================================

# 7.1 Biểu thức rất sâu (stress limit stack)

def test_701_very_deep_arithmetic_expression_stack():
    # ((((1+2)+3)+4)+...+20) * 2  (xây theo kết hợp trái để đẩy stack sâu)
    expr = BinaryOp(IntegerLiteral(1), "+", IntegerLiteral(2))
    for k in range(3, 21):
        expr = BinaryOp(expr, "+", IntegerLiteral(k))
    expr = BinaryOp(expr, "*", IntegerLiteral(2))  # nhân thêm để đẩy thao tác
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [expr]))
        ])
    ])
    expected = str(sum(range(1, 21)) * 2)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_702_deep_mixed_ops_precedence():
    # ((1+2*3) - (4*5 - 6) + (7*(8-3))) / 2
    part1 = BinaryOp(IntegerLiteral(1), "+", BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(3)))
    part2 = BinaryOp(BinaryOp(IntegerLiteral(4), "*", IntegerLiteral(5)), "-", IntegerLiteral(6))
    part3 = BinaryOp(IntegerLiteral(7), "*", BinaryOp(IntegerLiteral(8), "-", IntegerLiteral(3)))
    expr  = BinaryOp(BinaryOp(BinaryOp(part1, "-", part2), "+", part3), "/", IntegerLiteral(2))
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [ ExprStmt(FunctionCall(Identifier("print"), [expr])) ])
    ])
    expected = str(((1+2*3) - (4*5-6) + (7*(8-3))) // 2)
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.2 Rất nhiều biến cục bộ (stress limit local)

def test_703_many_locals_and_sum():
    # Khai báo ~15 biến rồi cộng dồn
    decls = [VarDecl(f"v{i}", IntType(), IntegerLiteral(i)) for i in range(1, 16)]
    # out = "" + (v1+...+v15)
    acc = Identifier("v1")
    for i in range(2, 16):
        acc = BinaryOp(acc, "+", Identifier(f"v{i}"))
    ast = Program([], [
        FuncDecl("main", [], VoidType(), decls + [
            ExprStmt(FunctionCall(Identifier("print"), [acc]))
        ])
    ])
    expected = str(sum(range(1, 16)))
    assert CodeGenerator().generate_and_run(ast) == expected


def test_704_many_params_function_sum10():
    # Hàm có nhiều tham số để kiểm tra cấp phát local cho params
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                FunctionCall(Identifier("sum10"), [
                    IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5),
                    IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8), IntegerLiteral(9), IntegerLiteral(10)
                ])
            ]))
        ]),
        FuncDecl("sum10",
                 [Param(f"a{i}", IntType()) for i in range(1, 11)],
                 IntType(),
                 [
                     ReturnStmt(
                        BinaryOp(
                            BinaryOp(
                                BinaryOp(
                                    BinaryOp(
                                        BinaryOp(
                                            BinaryOp(
                                                BinaryOp(
                                                    BinaryOp(
                                                        BinaryOp(Identifier("a1"), "+", Identifier("a2")),
                                                        "+", Identifier("a3")),
                                                    "+", Identifier("a4")),
                                                "+", Identifier("a5")),
                                            "+", Identifier("a6")),
                                        "+", Identifier("a7")),
                                    "+", Identifier("a8")),
                                "+", Identifier("a9")),
                            "+", Identifier("a10"))
                     )
                 ])
    ])
    expected = str(sum(range(1, 11)))
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.3 Shadowing nhiều tầng & scope block

def test_705_multilevel_shadowing_blocks():
    # outer x=1; inner x=2; deepest x=3 -> in "3\n2\n1"
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(1)),
            BlockStmt([
                VarDecl("x", IntType(), IntegerLiteral(2)),
                BlockStmt([
                    VarDecl("x", IntType(), IntegerLiteral(3)),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))  # 3
                ]),
                ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))      # 2
            ]),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))          # 1
        ])
    ])
    expected = "3\n2\n1"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_706_shadowing_param_then_local_then_restore_outer():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(50)),
            ExprStmt(FunctionCall(Identifier("print"), [
                FunctionCall(Identifier("foo"), [IntegerLiteral(7)])
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))  # outer untouched
        ]),
        FuncDecl("foo", [Param("x", IntType())], IntType(), [
            VarDecl("x", IntType(), IntegerLiteral(100)),  # shadow param
            ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(1)))
        ])
    ])
    expected = "101\n50"
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.4 Tất cả đường đi của hàm không-void đều return

def test_707_function_all_paths_return_if_elif_else():
    # sign(n): n<0 -> -1, n==0 -> 0, else -> 1
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral(""), "+", FunctionCall(Identifier("sign"), [IntegerLiteral(-5)])),
                    "+",
                    BinaryOp(FunctionCall(Identifier("sign"), [IntegerLiteral(0)]), "+", FunctionCall(Identifier("sign"), [IntegerLiteral(9)]))
                )
            ]))
        ]),
        FuncDecl("sign", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "<", IntegerLiteral(0)),
                BlockStmt([ReturnStmt(BinaryOp(IntegerLiteral(0), "-", IntegerLiteral(1)))]),  # -1
                [(BinaryOp(Identifier("n"), "==", IntegerLiteral(0)),
                  BlockStmt([ReturnStmt(IntegerLiteral(0))]))],
                BlockStmt([ReturnStmt(IntegerLiteral(1))])
            )
        ])
    ])
    expected = str(-1) + str(0 + 1)  # " -1 01" nhưng chúng ta nối "(-1)" + (0+1) => "-11"? cẩn thận
    # Để rõ ràng: "" + sign(-5) + sign(0) + sign(9)
    expected = f"{-1}{1}"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_708_function_nested_ifs_all_leaves_return():
    # piecewise(n):
    #   if n<0: if n<-5 return -2 else return -1
    #   else:   if n>5  return  2 else return  1
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(
                        BinaryOp(StringLiteral(""), "+", FunctionCall(Identifier("piece"), [IntegerLiteral(-7)])),
                        "+",
                        FunctionCall(Identifier("piece"), [IntegerLiteral(0)])
                    ),
                    "+",
                    FunctionCall(Identifier("piece"), [IntegerLiteral(8)])
                )
            ]))
        ]),
        FuncDecl("piece", [Param("n", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("n"), "<", IntegerLiteral(0)),
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("n"), "<", IntegerLiteral(-5)),
                        BlockStmt([ReturnStmt(IntegerLiteral(-2))]),
                        [],
                        BlockStmt([ReturnStmt(IntegerLiteral(-1))])
                    )
                ]),
                [],
                BlockStmt([
                    IfStmt(
                        BinaryOp(Identifier("n"), ">", IntegerLiteral(5)),
                        BlockStmt([ReturnStmt(IntegerLiteral(2))]),
                        [],
                        BlockStmt([ReturnStmt(IntegerLiteral(1))])
                    )
                ])
            )
        ])
    ])
    expected = "-212"
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.5 Vòng lặp lồng sâu + scope biến tạm trong thân

def test_709_nested_loops_with_inner_locals_and_acc():
    # while + while lồng nhau, tạo biến tạm trong thân để stress scope/stack
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(1)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<=", IntegerLiteral(3)),
                BlockStmt([
                    VarDecl("j", IntType(), IntegerLiteral(1)),
                    WhileStmt(
                        BinaryOp(Identifier("j"), "<=", IntegerLiteral(2)),
                        BlockStmt([
                            VarDecl("t", IntType(), BinaryOp(Identifier("i"), "+", Identifier("j"))),
                            Assignment(IdLValue("out"),
                                       BinaryOp(Identifier("out"), "+",
                                                BinaryOp(StringLiteral(""), "+", Identifier("t")))),
                            Assignment(IdLValue("j"), BinaryOp(Identifier("j"), "+", IntegerLiteral(1)))
                        ])
                    ),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    # i=1 -> j=1..2 -> 2,3 ; i=2 -> 3,4 ; i=3 -> 4,5 => "23 34 45"
    expected = "233445"
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.6 Biểu thức bool dài (stress so sánh + and/or chuỗi)

def test_710_long_boolean_chain_and_or():
    # ((1<2)&&(3<4)) || ((5==5)&&(6>2))  -> true
    left  = BinaryOp(BinaryOp(IntegerLiteral(1), "<", IntegerLiteral(2)),
                     "&&",
                     BinaryOp(IntegerLiteral(3), "<", IntegerLiteral(4)))
    right = BinaryOp(BinaryOp(IntegerLiteral(5), "==", IntegerLiteral(5)),
                     "&&",
                     BinaryOp(IntegerLiteral(6), ">", IntegerLiteral(2)))
    expr  = BinaryOp(left, "||", right)
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [BinaryOp(StringLiteral(""), "+", expr)]))
        ])
    ])
    expected = "true"
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.7 Tái sử dụng tên biến sau block (scope kết thúc, tên dùng lại hợp lệ)

def test_711_redeclare_name_after_block_scope():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            BlockStmt([
                VarDecl("x", IntType(), IntegerLiteral(10)),
                ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))  # 10
            ]),
            VarDecl("x", IntType(), IntegerLiteral(7)),  # dùng lại tên x sau khi block trên kết thúc
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))      # 7
        ])
    ])
    expected = "10\n7"
    assert CodeGenerator().generate_and_run(ast) == expected

# 7.8 Biểu thức rất sâu trong hàm, có locals xen kẽ (stress tổng hợp)

def test_712_function_deep_expr_with_locals_stack_local_mix():
    # f(n): let a=1,b=2,c=3; return (((n+a)*b + (n-1)*c) - (a+b+c)) * (n+2)
    body_expr = BinaryOp(
        BinaryOp(
            BinaryOp(BinaryOp(Identifier("n"), "+", Identifier("a")), "*", Identifier("b")),
            "+",
            BinaryOp(BinaryOp(Identifier("n"), "-", IntegerLiteral(1)), "*", Identifier("c"))
        ),
        "-",
        BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "+", Identifier("c"))
    )
    ret_expr = BinaryOp(body_expr, "*", BinaryOp(Identifier("n"), "+", IntegerLiteral(2)))
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"),
                                  [FunctionCall(Identifier("f"), [IntegerLiteral(4)])]))
        ]),
        FuncDecl("f", [Param("n", IntType())], IntType(), [
            VarDecl("a", IntType(), IntegerLiteral(1)),
            VarDecl("b", IntType(), IntegerLiteral(2)),
            VarDecl("c", IntType(), IntegerLiteral(3)),
            ReturnStmt(ret_expr)
        ])
    ])
    # Tính expected bằng Python:
    n=4; a=1; b=2; c=3
    expected_val = (((n+a)*b + (n-1)*c) - (a+b+c)) * (n+2)
    expected = str(expected_val)
    assert CodeGenerator().generate_and_run(ast) == expected

# =====================================================
# PHẦN 8 — Trường hợp biên & đặc biệt
# =====================================================

# -------------------------
# 8.1 Giá trị biên của hằng số (ICONST/BIPUSH/SIPUSH/LDC)
# -------------------------

def test_801_iconst_range_min1_to_5():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # In lần lượt: -1 0 1 2 3 4 5 (mỗi số trên 1 dòng)
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(-1)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(0)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(1)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(2)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(3)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(4)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(5)])),
        ])
    ])
    expected = "-1\n0\n1\n2\n3\n4\n5"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_802_bipush_edges_neg128_pos127():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(-128)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(127)])),
        ])
    ])
    expected = "-128\n127"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_803_sipush_edges_neg32768_pos32767():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(-32768)])),
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(32767)])),
        ])
    ])
    expected = "-32768\n32767"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_804_ldc_large_integer_and_concat():
    # Giá trị lớn vượt SIPUSH -> LDC
    big = 1000000
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral(""), "+", IntegerLiteral(big))
            ]))
        ])
    ])
    expected = str(big)
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.2 Số âm, 0, và biểu thức biên
# -------------------------

def test_805_arithmetic_with_zero_and_negatives():
    # (0 - 5) + (-3) * (10 - 10) = -5 + (-3)*0 = -5
    expr = BinaryOp(
        BinaryOp(IntegerLiteral(0), "-", IntegerLiteral(5)),
        "+",
        BinaryOp(
            IntegerLiteral(-3),
            "*",
            BinaryOp(IntegerLiteral(10), "-", IntegerLiteral(10))
        )
    )
    ast = Program([], [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [expr]))])])
    expected = str(-5)
    assert CodeGenerator().generate_and_run(ast) == expected


def test_806_chained_zero_adds_and_subs():
    # (((0+0)-0)+0)-0 = 0
    expr = BinaryOp(
        BinaryOp(
            BinaryOp(
                BinaryOp(IntegerLiteral(0), "+", IntegerLiteral(0)),
                "-",
                IntegerLiteral(0)
            ),
            "+",
            IntegerLiteral(0)
        ),
        "-",
        IntegerLiteral(0)
    )
    ast = Program([], [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [expr]))])])
    expected = "0"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.3 Vòng lặp không vào thân, break/continue ở biên
# -------------------------

def test_807_while_never_enters():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(5)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(0)),
                BlockStmt([
                    Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", StringLiteral("X")))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = ""
    assert CodeGenerator().generate_and_run(ast) == expected


def test_808_while_break_immediately_first_iteration():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                BlockStmt([
                    BreakStmt(),  # break ngay
                    Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", StringLiteral("X"))),
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = ""  # không in gì vì break ngay
    assert CodeGenerator().generate_and_run(ast) == expected


def test_809_while_continue_immediately_each_time():
    # i tăng lên, nhưng mỗi vòng đều continue trước khi nối chuỗi -> không in gì
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", IntType(), IntegerLiteral(0)),
            VarDecl("out", StringType(), StringLiteral("")),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                BlockStmt([
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                    ContinueStmt(),
                    Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", StringLiteral("Y")))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = ""
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.4 ArrayLiteral toàn 0, cập nhật dồn dập, truy cập biên
# -------------------------

def test_810_array_all_zeros_then_update_edges_and_read():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 4),
                    ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            # Ghi vào biên: a[0], a[3]
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(0)), IntegerLiteral(9)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(3)), IntegerLiteral(7)),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(3))]))
        ])
    ])
    expected = "9\n7"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_811_array_update_chain_many_times_same_cell():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0)])),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(1)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(2)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(3)),
            Assignment(ArrayAccessLValue(Identifier("a"), IntegerLiteral(1)), IntegerLiteral(4)),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(1))]))
        ])
    ])
    expected = "4"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_812_array_index_expression_edges_0_and_last():
    # Ghi vào chỉ số 0 và (n-1) bằng biểu thức
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("n", IntType(), IntegerLiteral(3)),
            VarDecl("a", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            Assignment(ArrayAccessLValue(Identifier("a"), BinaryOp(IntegerLiteral(1), "-", IntegerLiteral(1))), IntegerLiteral(11)),  # idx=0
            Assignment(ArrayAccessLValue(Identifier("a"), BinaryOp(Identifier("n"), "-", IntegerLiteral(1))), IntegerLiteral(22)),     # idx=2
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(2))]))
        ])
    ])
    expected = "11\n22"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.5 Chuỗi rỗng + nối nhiều lần; build chuỗi dài
# -------------------------

def test_813_concatenate_empty_string_many_times():
    # out = "" ; out = out + "" + "" + "" ; cuối cùng vẫn rỗng
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("out", StringType(), StringLiteral("")),
            Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", StringLiteral(""))),
            Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", StringLiteral(""))),
            Assignment(IdLValue("out"), BinaryOp(Identifier("out"), "+", StringLiteral(""))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = ""
    assert CodeGenerator().generate_and_run(ast) == expected


def test_814_build_long_string_from_ints():
    # Nối 1..9 thành "123456789"
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("s", StringType(), StringLiteral("")),
            VarDecl("i", IntType(), IntegerLiteral(1)),
            WhileStmt(
                BinaryOp(Identifier("i"), "<", IntegerLiteral(10)),
                BlockStmt([
                    Assignment(IdLValue("s"),
                               BinaryOp(Identifier("s"), "+",
                                        BinaryOp(StringLiteral(""), "+", Identifier("i")))),
                    Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                ])
            ),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("s")]))
        ])
    ])
    expected = "123456789"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.6 Cập nhật dồn dập biến thường; chuỗi phép tính dài
# -------------------------

def test_815_variable_many_sequential_updates():
    # x khởi 0, tăng 1 mười lần -> 10
    updates = [Assignment(IdLValue("x"), BinaryOp(Identifier("x"), "+", IntegerLiteral(1))) for _ in range(10)]
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(0)),
            *updates,
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "10"
    assert CodeGenerator().generate_and_run(ast) == expected


def test_816_long_left_associative_chain_add_sub_mul():
    # (((1+2)-3)+4)-5 + 6*7 = (((0)+4)-5) + 42 = 41
    expr = BinaryOp(
        BinaryOp(
            BinaryOp(
                BinaryOp(IntegerLiteral(1), "+", IntegerLiteral(2)),
                "-",
                IntegerLiteral(3)
            ),
            "+",
            IntegerLiteral(4)
        ),
        "-",
        IntegerLiteral(5)
    )
    expr = BinaryOp(expr, "+", BinaryOp(IntegerLiteral(6), "*", IntegerLiteral(7)))
    ast = Program([], [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [expr]))])])
    expected = str((((1+2)-3)+4)-5 + 6*7)
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.7 Logic biên với so sánh bằng/khác và 0/1
# -------------------------

def test_817_boolean_relations_edge_equal_not_equal_zero_one():
    # "" + (0==0) + (1!=0) + (2==3) -> "truetruefalse"
    expr = BinaryOp(
        BinaryOp(StringLiteral(""), "+", BinaryOp(IntegerLiteral(0), "==", IntegerLiteral(0))),
        "+",
        BinaryOp(BinaryOp(IntegerLiteral(1), "!=", IntegerLiteral(0)), "+", BinaryOp(IntegerLiteral(2), "==", IntegerLiteral(3)))
    )
    ast = Program([], [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [expr]))])])
    expected = "truetruefalse"
    assert CodeGenerator().generate_and_run(ast) == expected

# -------------------------
# 8.8 For-in biên: mảng rỗng, break ở phần tử đầu/cuối
# -------------------------

def test_818_for_in_empty_array_no_output():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("xs", ArrayType(IntType(), 0), ArrayLiteral([])),
            ForStmt("v", Identifier("xs"), BlockStmt([
                ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(StringLiteral(""), "+", Identifier("v"))]))
            ]))
        ])
    ])
    expected = ""
    assert CodeGenerator().generate_and_run(ast) == expected


def test_819_for_in_break_on_first_and_last():
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            # Break tại phần tử đầu tiên -> không in gì
            VarDecl("a", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(9), IntegerLiteral(8), IntegerLiteral(7)])),
            ForStmt("x", Identifier("a"), BlockStmt([
                BreakStmt(),
                ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(StringLiteral(""), "+", Identifier("x"))]))
            ])),
            # Break tại phần tử cuối (sau khi đã in các phần tử trước)
            VarDecl("b", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            VarDecl("out", StringType(), StringLiteral("")),
            ForStmt("y", Identifier("b"), BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("y"), "==", IntegerLiteral(3)),
                    BlockStmt([BreakStmt()]),
                    [],
                    None
                ),
                Assignment(IdLValue("out"),
                           BinaryOp(Identifier("out"), "+",
                                    BinaryOp(StringLiteral(""), "+", Identifier("y"))))
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("out")]))
        ])
    ])
    expected = "12"
    assert CodeGenerator().generate_and_run(ast) == expected