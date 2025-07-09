from utils import ASTGenerator


def test_001():
    """Test basic constant declaration AST generation"""
    source = "const x: int = 42;"
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(42))])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_002():
    """Test function declaration AST generation"""
    source = "func main() -> void {};"
    expected = "Program(funcs=[FuncDecl(main, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test function with parameters AST generation"""
    source = "func add(a: int, b: int) -> int { return a + b; };"
    expected = "Program(funcs=[FuncDecl(add, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test multiple declarations AST generation"""
    source = """const PI: float = 3.14;
    func square(x: int) -> int { return x * x; };"""
    expected = "Program(consts=[ConstDecl(PI, float, FloatLiteral(3.14))], funcs=[FuncDecl(square, [Param(x, int)], int, [ReturnStmt(BinaryOp(Identifier(x), *, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(name, StringLiteral('Alice'))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """func main() -> void { 
        if (x > 0) { 
            return x;
        } else { 
            return 0;
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([ReturnStmt(Identifier(x))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    """Test while loop AST generation"""
    source = """func main() -> void { 
        while (i < 10) { 
            i = i + 1; 
        }
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_008():
    """Test array operations AST generation"""
    source = """func main() -> void { 
        let arr = [1, 2, 3];
        let first = arr[0];
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])), VarDecl(first, ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    """Test pipeline operator AST generation"""
    source = """func main() -> void { 
        let result = data >> process;
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(Identifier(data), >>, Identifier(process)))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_string_literal():
    """Test basic string literal AST generation"""
    source = """func main() -> void {
        let name: string = "Alice";
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(name, string, StringLiteral('Alice'))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_string_concatenation():
    """Test string concatenation AST generation"""
    source = """func main() -> void {
        let greeting = "Hello, " + name;
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(greeting, BinaryOp(StringLiteral('Hello, '), +, Identifier(name)))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_array_indexing():
    source = """func main() -> void {
        let x = arr[2];
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, ArrayAccess(Identifier(arr), IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_function_with_void_return():
    source = """func log(msg: string) -> void {
        print(msg);
    };"""
    expected = "Program(funcs=[FuncDecl(log, [Param(msg, string)], void, [ExprStmt(FunctionCall(Identifier(print), [Identifier(msg)]))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_nested_function_call():
    source = """func main() -> void {
        let res = format(getUser(id));
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(res, FunctionCall(Identifier(format), [FunctionCall(Identifier(getUser), [Identifier(id)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_pipeline_operator():
    source = """func main() -> void {
        let r = data >> normalize >> analyze;
    };"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(r, BinaryOp(BinaryOp(Identifier(data), >>, Identifier(normalize)), >>, Identifier(analyze)))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_anonymous_function():
    source = """func main() {
    let f = func(x: int) -> int { return x + 1; };
    let result = f(5);
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(f, BlockStmt([ReturnStmt(BinaryOp(Identifier(x), +, IntegerLiteral(1)))])), VarDecl(result, FunctionCall(Identifier(f), [IntegerLiteral(5)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_301():
    """Test local variable declaration in main function"""
    source = """func main() -> void {
    let x: int = 0;
}"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_302():
    """Test const declaration followed by void main"""
    source = """const x: int = 42;
                func main() -> void { return; }"""
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(42))], funcs=[FuncDecl(main, [], void, [ReturnStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_303():
    """Test function returning an array literal"""
    source = """func votien() -> void {
    return [1, 2, 3];
}"""
    expected = "Program(funcs=[FuncDecl(votien, [], void, [ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_304():
    """Test nested function call as expression"""
    source = """func main() -> void {
    bar(foo(p), 1);
}"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(bar), [FunctionCall(Identifier(foo), [Identifier(p)]), IntegerLiteral(1)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_305():
    """Test if-else control flow returning literals"""
    source = """func test() -> void {
    if (a > b) {
        return 1;
    } else {
        return 0;
    }
}"""
    expected = "Program(funcs=[FuncDecl(test, [], void, [IfStmt(condition=BinaryOp(Identifier(a), >, Identifier(b)), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_306():
    """Test increment logic with variable assignment"""
    source = """func doSomething() -> void {
    let s: int = 10;
    s = s + 1;
}"""
    expected = "Program(funcs=[FuncDecl(doSomething, [], void, [VarDecl(s, int, IntegerLiteral(10)), Assignment(IdLValue(s), BinaryOp(Identifier(s), +, IntegerLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_307():
    """Test return expression with modulo and comparison"""
    source = """func main() -> void {
    return n % 2 == 0;
}"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ReturnStmt(BinaryOp(BinaryOp(Identifier(n), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_308():
    """Test function isEven with bool return"""
    source = """func isEven(n: int) -> bool {
    return n % 2 == 0;
}"""
    expected = "Program(funcs=[FuncDecl(isEven, [Param(n, int)], bool, [ReturnStmt(BinaryOp(BinaryOp(Identifier(n), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_309():
    """Test function with if-condition and return in both branches"""
    source = """func main() -> int {
    let x: int = 5;
    if (isEven(x)) {
        return 1;
    } else {
        return 0;
    }
}"""
    expected = "Program(funcs=[FuncDecl(main, [], int, [VarDecl(x, int, IntegerLiteral(5)), IfStmt(condition=FunctionCall(Identifier(isEven), [Identifier(x)]), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_310():
    """Test nested function call in if condition"""
    source = """func main() -> int {
    let x: int = 5;
    if (isEven(myMethod(hello), x)) {
        return 1;
    } else {
        return 0;
    }
}"""
    expected = "Program(funcs=[FuncDecl(main, [], int, [VarDecl(x, int, IntegerLiteral(5)), IfStmt(condition=FunctionCall(Identifier(isEven), [FunctionCall(Identifier(myMethod), [Identifier(hello)]), Identifier(x)]), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_311():
    """Test hàm isEven và if-else trả về chuỗi"""
    source = """func isEven(n: int) -> bool {
    return n % 2 == 0;
}
func main() -> string {
    let x: int = 5;
    if (isEven(x)) {
        return "So chan";
    } else {
        return "So le";
    }
}"""
    expected = (
        "Program(funcs=["
        "FuncDecl(isEven, [Param(n, int)], bool, ["
            "ReturnStmt(BinaryOp(BinaryOp(Identifier(n), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))"
        "]), "
        "FuncDecl(main, [], string, ["
            "VarDecl(x, int, IntegerLiteral(5)), "
            "IfStmt(condition=FunctionCall(Identifier(isEven), [Identifier(x)]), "
                "then_stmt=BlockStmt([ReturnStmt(StringLiteral('So chan'))]), "
                "else_stmt=BlockStmt([ReturnStmt(StringLiteral('So le'))]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_312():
    """Test return; trong hàm void"""
    source = """func main() -> void {
    return;
}"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ReturnStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_313():
    """Test while loop tính tổng từ 1 đến n"""
    source = """func main() -> void {
    let n: int = 10;
    let sum: int = 0;
    let i: int = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
            "VarDecl(n, int, IntegerLiteral(10)), "
            "VarDecl(sum, int, IntegerLiteral(0)), "
            "VarDecl(i, int, IntegerLiteral(1)), "
            "WhileStmt(BinaryOp(Identifier(i), <=, Identifier(n)), "
                "BlockStmt(["
                    "Assignment(IdLValue(sum), BinaryOp(Identifier(sum), +, Identifier(i))), "
                    "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
                "])"
            ")"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_314():
    """Test if-else gán boolean"""
    source = """func main() -> void {
    let x: int = 7;
    let result: bool = false;
    if (isEven(x)) {
        result = true;
    } else {
        result = false;
    }
}"""
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
            "VarDecl(x, int, IntegerLiteral(7)), "
            "VarDecl(result, bool, BooleanLiteral(False)), "
            "IfStmt(condition=FunctionCall(Identifier(isEven), [Identifier(x)]), "
                "then_stmt=BlockStmt([Assignment(IdLValue(result), BooleanLiteral(True))]), "
                "else_stmt=BlockStmt([Assignment(IdLValue(result), BooleanLiteral(False))]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_315():
    """Test khởi tạo và xử lý mảng với while"""
    source = """func main() -> void {
    let arr: [int; 5] = [0, 0, 0, 0, 0];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    arr[3] = 4;
    arr[4] = 5;

    let reversed: [int; 5] = [0, 0, 0, 0, 0];
    let i: int = 4;
    let j: int = 0;
    while (i < 10) {
        reversed[j] = arr[i];
        i = i - 1;
        j = j + 1;
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
            "VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(2)), IntegerLiteral(3)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(3)), IntegerLiteral(4)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(4)), IntegerLiteral(5)), "
            "VarDecl(reversed, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "VarDecl(i, int, IntegerLiteral(4)), "
            "VarDecl(j, int, IntegerLiteral(0)), "
            "WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), "
                "BlockStmt(["
                    "Assignment(ArrayAccessLValue(Identifier(reversed), Identifier(j)), ArrayAccess(Identifier(arr), Identifier(i))), "
                    "Assignment(IdLValue(i), BinaryOp(Identifier(i), -, IntegerLiteral(1))), "
                    "Assignment(IdLValue(j), BinaryOp(Identifier(j), +, IntegerLiteral(1))), "
                    "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
                "])"
            ")"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_316():
    """Test đệ quy tính factorial với if-base-case"""
    source = """func factorial(n: int) -> int {
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}"""
    expected = (
        "Program(funcs=["
        "FuncDecl(factorial, [Param(n, int)], int, ["
            "IfStmt(condition=BinaryOp(Identifier(n), ==, IntegerLiteral(0)), "
                "then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))])), "
            "ReturnStmt(BinaryOp(Identifier(n), *, FunctionCall(Identifier(factorial), [BinaryOp(Identifier(n), -, IntegerLiteral(1))])))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_317():
    """Test for-in với if và elif"""
    source = """func main() -> void {
    for (value in myArr) {
        if (arr[i] < firstMin) {
            secondMin = firstMin;
            firstMin = arr[i];
        } else if ((arr[i] < secondMin) && (arr[i] != firstMin)) {
            secondMin = arr[i];
        }
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [ForStmt(value, Identifier(myArr), BlockStmt([IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(firstMin)), then_stmt=BlockStmt([Assignment(IdLValue(secondMin), Identifier(firstMin)), Assignment(IdLValue(firstMin), ArrayAccess(Identifier(arr), Identifier(i)))]), elif_branches=[(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(secondMin)), &&, BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), !=, Identifier(firstMin))), BlockStmt([Assignment(IdLValue(secondMin), ArrayAccess(Identifier(arr), Identifier(i)))]))]), Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_318():
    """Test for-in đơn giản chỉ tăng i"""
    source = """func main() -> void {
    for (value in myArr) {
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
            "ForStmt(value, Identifier(myArr), BlockStmt(["
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_319():
    """Test hai hàm main liên tiếp với for-in và if-elif"""
    source = """func main() -> void {
    for (value in myArr) {
        i = i + 1;
    }
}

func main() -> void {
    for (value in myArr) {
        if (arr[i] < firstMin) {
            secondMin = firstMin;
            firstMin = arr[i];
        } else if ((arr[i] < secondMin) && (arr[i] != firstMin)) {
            secondMin = arr[i];
        }
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
        # Hàm đầu
        "FuncDecl(main, [], void, ["
            "ForStmt(value, Identifier(myArr), BlockStmt(["
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
        "]), "
        # Hàm thứ hai
        "FuncDecl(main, [], void, ["
            "ForStmt(value, Identifier(myArr), BlockStmt(["
                "IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(firstMin)), "
                    "then_stmt=BlockStmt(["
                        "Assignment(IdLValue(secondMin), Identifier(firstMin)), "
                        "Assignment(IdLValue(firstMin), ArrayAccess(Identifier(arr), Identifier(i)))"
                    "]), "
                    "elif_branches=[(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(secondMin)), &&, BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), !=, Identifier(firstMin))), BlockStmt([Assignment(IdLValue(secondMin), ArrayAccess(Identifier(arr), Identifier(i)))]))]"
                "), "
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_320():
    """Test ba hàm main: hai for-in và một xử lý mảng với while"""
    source = """func main() -> void {
    for (value in myArr) {
        i = i + 1;
    }
}

func main() -> void {
    for (value in myArr) {
        if (arr[i] < firstMin) {
            secondMin = firstMin;
            firstMin = arr[i];
        } else if ((arr[i] < secondMin) && (arr[i] != firstMin)) {
            secondMin = arr[i];
        }
        i = i + 1;
    }
}

func main() -> void {
    let arr: [int; 5] = [0, 0, 0, 0, 0];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    arr[3] = 4;
    arr[4] = 5;

    let reversed: [int; 5] = [0, 0, 0, 0, 0];
    let i: int = 4;
    let j: int = 0;
    while (i < 10) {
        reversed[j] = arr[i];
        i = i - 1;
        j = j + 1;
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
        # Hàm 1
        "FuncDecl(main, [], void, ["
            "ForStmt(value, Identifier(myArr), BlockStmt(["
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
        "]), "
        # Hàm 2
        "FuncDecl(main, [], void, ["
            "ForStmt(value, Identifier(myArr), BlockStmt(["
                "IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(firstMin)), "
                    "then_stmt=BlockStmt(["
                        "Assignment(IdLValue(secondMin), Identifier(firstMin)), "
                        "Assignment(IdLValue(firstMin), ArrayAccess(Identifier(arr), Identifier(i)))"
                    "]), "
                    "elif_branches=[(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(secondMin)), &&, BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), !=, Identifier(firstMin))), BlockStmt([Assignment(IdLValue(secondMin), ArrayAccess(Identifier(arr), Identifier(i)))]))]"
                "), "
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
        "]), "
        # Hàm 3
        "FuncDecl(main, [], void, ["
            "VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(2)), IntegerLiteral(3)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(3)), IntegerLiteral(4)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(4)), IntegerLiteral(5)), "
            "VarDecl(reversed, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "VarDecl(i, int, IntegerLiteral(4)), "
            "VarDecl(j, int, IntegerLiteral(0)), "
            "WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt(["
                "Assignment(ArrayAccessLValue(Identifier(reversed), Identifier(j)), ArrayAccess(Identifier(arr), Identifier(i))), "
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), -, IntegerLiteral(1))), "
                "Assignment(IdLValue(j), BinaryOp(Identifier(j), +, IntegerLiteral(1))), "
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_321():
    """Test khởi tạo và xử lý mảng với while (full)"""
    source = """func main() -> void {
    let arr: [int; 5] = [0, 0, 0, 0, 0];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    arr[3] = 4;
    arr[4] = 5;

    let reversed: [int; 5] = [0, 0, 0, 0, 0];
    let i: int = 4;
    let j: int = 0;
    while (i < 10) {
        reversed[j] = arr[i];
        i = i - 1;
        j = j + 1;
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(main, [], void, ["
            "VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(2)), IntegerLiteral(3)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(3)), IntegerLiteral(4)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(4)), IntegerLiteral(5)), "
            "VarDecl(reversed, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "VarDecl(i, int, IntegerLiteral(4)), "
            "VarDecl(j, int, IntegerLiteral(0)), "
            "WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt(["
              "Assignment(ArrayAccessLValue(Identifier(reversed), Identifier(j)), ArrayAccess(Identifier(arr), Identifier(i))), "
              "Assignment(IdLValue(i), BinaryOp(Identifier(i), -, IntegerLiteral(1))), "
              "Assignment(IdLValue(j), BinaryOp(Identifier(j), +, IntegerLiteral(1))), "
              "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_322():
    """Test lặp lại test_321 để chắc chắn tính ổn định"""
    source = """func main() -> void {
    let arr: [int; 5] = [0, 0, 0, 0, 0];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    arr[3] = 4;
    arr[4] = 5;

    let reversed: [int; 5] = [0, 0, 0, 0, 0];
    let i: int = 4;
    let j: int = 0;
    while (i < 10) {
        reversed[j] = arr[i];
        i = i - 1;
        j = j + 1;
        i = i + 1;
    }
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(main, [], void, ["
            "VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(2)), IntegerLiteral(3)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(3)), IntegerLiteral(4)), "
            "Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(4)), IntegerLiteral(5)), "
            "VarDecl(reversed, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
            "VarDecl(i, int, IntegerLiteral(4)), "
            "VarDecl(j, int, IntegerLiteral(0)), "
            "WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt(["
              "Assignment(ArrayAccessLValue(Identifier(reversed), Identifier(j)), ArrayAccess(Identifier(arr), Identifier(i))), "
              "Assignment(IdLValue(i), BinaryOp(Identifier(i), -, IntegerLiteral(1))), "
              "Assignment(IdLValue(j), BinaryOp(Identifier(j), +, IntegerLiteral(1))), "
              "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
            "]))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_323():
    """Test khai báo mảng kích thước 1 với initializer int"""
    source = """func foo() -> void {
    let a: [int; 1] = 1;
}"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(a, [int; 1], IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_324():
    """Test khai báo biến int không gán giá trị cụ thể (mặc định 0)"""
    source = """func foo() -> void {
    let a: int = 0;
}"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(a, int, IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_325():
    """Test các phép gán toán tử +, -, *, /, %"""
    source = """func foo() -> void {
    a = a + 1;
    a = a - 1;
    a = a * 1;
    a = a / 1;
    a = a % 1;
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(foo, [], void, ["
            "Assignment(IdLValue(a), BinaryOp(Identifier(a), +, IntegerLiteral(1))), "
            "Assignment(IdLValue(a), BinaryOp(Identifier(a), -, IntegerLiteral(1))), "
            "Assignment(IdLValue(a), BinaryOp(Identifier(a), *, IntegerLiteral(1))), "
            "Assignment(IdLValue(a), BinaryOp(Identifier(a), /, IntegerLiteral(1))), "
            "Assignment(IdLValue(a), BinaryOp(Identifier(a), %, IntegerLiteral(1)))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_326():
    """Test truy cập và gán phần tử mảng với biểu thức trong index"""
    source = """func foo() -> void {
    a[1 + 1] = 1;
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(foo, [], void, ["
            "Assignment(ArrayAccessLValue(Identifier(a), BinaryOp(IntegerLiteral(1), +, IntegerLiteral(1))), IntegerLiteral(1))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_327():
    """Test truy cập trường và mảng lồng nhau"""
    source = """func foo() -> void {
    a[2][2] = 1;
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(foo, [], void, ["
            "Assignment(ArrayAccessLValue(ArrayAccessLValue(Identifier(a), IntegerLiteral(2)), IntegerLiteral(2)), IntegerLiteral(1))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_328():
    """Test nested 2D array assignment với chỉ số phức tạp"""
    source = """func main() -> void {
    let a: [[int; 2]; 2] = [[1,2],[3,4]];
    a[1][0] = a[0][1] + a[1][1];
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(main, [], void, ["
            "VarDecl(a, [[int; 2]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])])), "
            "Assignment(ArrayAccessLValue(ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), IntegerLiteral(0)), "
              "BinaryOp(ArrayAccess(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1)), +, ArrayAccess(ArrayAccess(Identifier(a), IntegerLiteral(1)), IntegerLiteral(1))))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_329():
    """Test nested 3D array assignment với biểu thức trong chỉ số"""
    source = """func main() -> void {
    let t: [[[int; 2]; 2]; 2] = [[[1,2],[3,4]], [[5,6],[7,8]]];
    t[1][0][1] = t[0][1][0] * 2;
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(main, [], void, ["
            "VarDecl(t, [[[int; 2]; 2]; 2], ArrayLiteral(["
              "ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]), "
              "ArrayLiteral([ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6)]), ArrayLiteral([IntegerLiteral(7), IntegerLiteral(8)])])"
            "])), "
            "Assignment(ArrayAccessLValue(ArrayAccessLValue(ArrayAccessLValue(Identifier(t), IntegerLiteral(1)), IntegerLiteral(0)), IntegerLiteral(1)), "
              "BinaryOp(ArrayAccess(ArrayAccess(ArrayAccess(Identifier(t), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(0)), *, IntegerLiteral(2)))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_330():
    """Test gán mảng với chỉ số tính toán và gọi hàm trong RHS"""
    source = """func foo() -> int { return 42; }
func main() -> void {
    let a: [int; 3] = [10,20,30];
    let i: int = 1;
    a[(i + foo()) % 3] = foo() + a[2];
}"""
    expected = (
        "Program(funcs=["
          "FuncDecl(foo, [], int, [ReturnStmt(IntegerLiteral(42))]), "
          "FuncDecl(main, [], void, ["
            "VarDecl(a, [int; 3], ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])), "
            "VarDecl(i, int, IntegerLiteral(1)), "
            "Assignment(ArrayAccessLValue(Identifier(a), BinaryOp(BinaryOp(Identifier(i), +, FunctionCall(Identifier(foo), [])), %, IntegerLiteral(3))), "
              "BinaryOp(FunctionCall(Identifier(foo), []), +, ArrayAccess(Identifier(a), IntegerLiteral(2))))"
          "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

from utils import ASTGenerator

def test_331():
    source = """
        func foo(){
            break;
            continue;
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [BreakStmt(), ContinueStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_332():
    source = """
        func foo(){
            return;
            return foo() + 2;
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [ReturnStmt(), ReturnStmt(BinaryOp(FunctionCall(Identifier(foo), []), +, IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_333():
    source = """
        func foo(){
            foo();
            foo(foo(), 2);
            bar(baz(), qux(3));
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, ["
            "ExprStmt(FunctionCall(Identifier(foo), [])), "
            "ExprStmt(FunctionCall(Identifier(foo), [FunctionCall(Identifier(foo), []), IntegerLiteral(2)])), "
            "ExprStmt(FunctionCall(Identifier(bar), [FunctionCall(Identifier(baz), []), FunctionCall(Identifier(qux), [IntegerLiteral(3)])]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_334():
    source = """
        func foo(){
            if(1) {return;}
            if(1 + 1) {
                return 1;
                return;
            }
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, [IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()])), IfStmt(condition=BinaryOp(IntegerLiteral(1), +, IntegerLiteral(1)), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1)), ReturnStmt()]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_335():
    source = """
        func foo(){
            if(1) { return;
            } else if(1) {
                return 1;
                return ;
            } else {return;}

            if(1) {return;}
            else {
                return 1;
                return ;
            }
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, ["
            "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()]), "
                "elif_branches=[(IntegerLiteral(1), BlockStmt([ReturnStmt(IntegerLiteral(1)), ReturnStmt()]))], "
                "else_stmt=BlockStmt([ReturnStmt()])), "
            "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()]), "
                "else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1)), ReturnStmt()]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_336():
    source = """
        func foo(){
            if(1) {
                return 1;
            } else if(2) {
                return 2;
            } else if(3) {
                return 3;
            } else if(4) {
                return 4;
            }
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, ["
            "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), "
                "elif_branches=["
                    "(IntegerLiteral(2), BlockStmt([ReturnStmt(IntegerLiteral(2))])), "
                    "(IntegerLiteral(3), BlockStmt([ReturnStmt(IntegerLiteral(3))])), "
                    "(IntegerLiteral(4), BlockStmt([ReturnStmt(IntegerLiteral(4))]))"
                "]"
                ")"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_337():
    source = """
        func votien() {
            for (a in [1,2,3]) {
                return;
                return 1;
            }
            for (a in arr[2]) {
                return;
                return 1;
            }
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(votien, [], void, [ForStmt(a, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([ReturnStmt(), ReturnStmt(IntegerLiteral(1))])), ForStmt(a, ArrayAccess(Identifier(arr), IntegerLiteral(2)), BlockStmt([ReturnStmt(), ReturnStmt(IntegerLiteral(1))]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_338():
    source = """
        func votien() {
            for (index in [1,2,3]) {
                return;
                return 1;
            }
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(votien, [], void, [ForStmt(index, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([ReturnStmt(), ReturnStmt(IntegerLiteral(1))]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_339():
    source = """
        func foo(){
            arr[0][1];
            matrix[1][2][3];
        }
    """
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, [ArrayAccess(ArrayAccess(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), ArrayAccess(ArrayAccess(ArrayAccess(Identifier(matrix), IntegerLiteral(1)), IntegerLiteral(2)), IntegerLiteral(3))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_340():
    source = """func main() { 5 >> add(3) >> multiply(2); };"""
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, ["
            "BinaryOp(BinaryOp(IntegerLiteral(5), >>, FunctionCall(Identifier(add), [IntegerLiteral(3)])), >>, FunctionCall(Identifier(multiply), [IntegerLiteral(2)]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

from utils import ASTGenerator

def test_341():
    source = """
func fib(n: int) -> int {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(fib, [Param(n, int)], int, ["
            "IfStmt(condition=BinaryOp(Identifier(n), <, IntegerLiteral(2)), then_stmt=BlockStmt([ReturnStmt(Identifier(n))])), "
            "ReturnStmt(BinaryOp(FunctionCall(Identifier(fib), [BinaryOp(Identifier(n), -, IntegerLiteral(1))]), +, FunctionCall(Identifier(fib), [BinaryOp(Identifier(n), -, IntegerLiteral(2))])))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_342():
    source = """
func compute(a: int, b: int, c: int, d: int) -> int {
    return a + b * c >> d;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(compute, [Param(a, int), Param(b, int), Param(c, int), Param(d, int)], int, ["
            "ReturnStmt(BinaryOp(BinaryOp(Identifier(a), +, BinaryOp(Identifier(b), *, Identifier(c))), >>, Identifier(d)))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_343():
    source = """
func loopWhile(x: int) -> void {
    let i: int = 1;
    while (i < x) {
        i = i * 2;
    }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(loopWhile, [Param(x, int)], void, ["
            "VarDecl(i, int, IntegerLiteral(1)), "
            "WhileStmt(BinaryOp(Identifier(i), <, Identifier(x)), BlockStmt(["
                "Assignment(IdLValue(i), BinaryOp(Identifier(i), *, IntegerLiteral(2)))"
            "]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_344():
    source = """
func countElements(arr: [int;5]) -> int {
    let count: int = 0;
    for (v in arr) {
        count = count + 1;
    }
    return count;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(countElements, [Param(arr, [int; 5])], int, ["
            "VarDecl(count, int, IntegerLiteral(0)), "
            "ForStmt(v, Identifier(arr), BlockStmt([Assignment(IdLValue(count), BinaryOp(Identifier(count), +, IntegerLiteral(1)))])), "
            "ReturnStmt(Identifier(count))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_345():
    source = """
func nestedFor(mat: [[int;3];2]) -> int {
    let sum: int = 0;
    for (row in mat) {
        for (elem in row) {
            sum = sum + elem;
        }
    }
    return sum;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(nestedFor, [Param(mat, [[int; 3]; 2])], int, ["
            "VarDecl(sum, int, IntegerLiteral(0)), "
            "ForStmt(row, Identifier(mat), BlockStmt(["
                "ForStmt(elem, Identifier(row), BlockStmt([Assignment(IdLValue(sum), BinaryOp(Identifier(sum), +, Identifier(elem)))]))"
            "])), "
            "ReturnStmt(Identifier(sum))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_346():
    source = """
func declVars() -> void {
    let a = 1;
    let b: float = 2.0;
    let c: bool = true;
    let s: string = \"hi\";
}
"""
    expected = (
        "Program(funcs=[FuncDecl(declVars, [], void, [VarDecl(a, IntegerLiteral(1)), VarDecl(b, float, FloatLiteral(2.0)), VarDecl(c, bool, BooleanLiteral(True)), VarDecl(s, string, StringLiteral('hi'))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_347():
    source = """
func makeConsts() -> void {
    const PI: float = 3.14;
    const FLAG: bool = true;
    const N: int = 10;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(makeConsts, [], void, ["
            "ConstDecl(PI, float, FloatLiteral(3.14)), "
            "ConstDecl(FLAG, bool, BooleanLiteral(True)), "
            "ConstDecl(N, int, IntegerLiteral(10))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_348():
    source = """
func arrLit() -> [int;3] {
    return [1, 2, 3];
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(arrLit, [], [int; 3], ["
            "ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_349():
    source = """
func assignMulti() -> void {
    let m: [[[int;2];2];2] = [[[1,2],[3,4]], [[5,6],[7,8]]];
    m[1][0][1] = m[0][1][0] * 2;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(assignMulti, [], void, ["
            "VarDecl(m, [[[int; 2]; 2]; 2], ArrayLiteral([ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]), ArrayLiteral([ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6)]), ArrayLiteral([IntegerLiteral(7), IntegerLiteral(8)])])])), "
            "Assignment(ArrayAccessLValue(ArrayAccessLValue(ArrayAccessLValue(Identifier(m), IntegerLiteral(1)), IntegerLiteral(0)), IntegerLiteral(1)), BinaryOp(ArrayAccess(ArrayAccess(ArrayAccess(Identifier(m), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(0)), *, IntegerLiteral(2)))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_350():
    source = """
func callExpr() -> int {
    return max(min(5, 3), 4);
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(callExpr, [], int, ["
            "ReturnStmt(FunctionCall(Identifier(max), [FunctionCall(Identifier(min), [IntegerLiteral(5), IntegerLiteral(3)]), IntegerLiteral(4)]))"
        "])"
        "])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_351():
    source = """
func foo() -> void {
    a();
    a(1, 2);
    a(1);
    b();
    b(3, 4);
    b(5);
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "ExprStmt(FunctionCall(Identifier(a), [])), "
            "ExprStmt(FunctionCall(Identifier(a), [IntegerLiteral(1), IntegerLiteral(2)])), "
            "ExprStmt(FunctionCall(Identifier(a), [IntegerLiteral(1)])), "
            "ExprStmt(FunctionCall(Identifier(b), [])), "
            "ExprStmt(FunctionCall(Identifier(b), [IntegerLiteral(3), IntegerLiteral(4)])), "
            "ExprStmt(FunctionCall(Identifier(b), [IntegerLiteral(5)]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_352():
    source = """
func foo() -> void {
    if (a) { return; }
    if (b) { return; } else { return; }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "IfStmt(condition=Identifier(a), then_stmt=BlockStmt([ReturnStmt()])), "
            "IfStmt(condition=Identifier(b), then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([ReturnStmt()]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_353():
    source = """
func foo() -> void {
    for (x in [1, 2, 3]) { return; }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "ForStmt(x, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([ReturnStmt()]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_354():
    source = """
func foo() -> void {
    for (v in [true, false]) { continue; }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "ForStmt(v, ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False)]), BlockStmt([ContinueStmt()]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_355():
    source = """
func foo() -> void {
    while (i < 10) { i = i + 1; }
}
"""
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, [WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_356():
    source = """
func foo() -> void {
    let a: int = 1;
    while (a <= 5) {
        a = a * 2;
    }
    let b: int = 2;
    while (b >= 1) {
        b = b / 2;
    }
}
"""
    expected = (
        "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(a, int, IntegerLiteral(1)), WhileStmt(BinaryOp(Identifier(a), <=, IntegerLiteral(5)), BlockStmt([Assignment(IdLValue(a), BinaryOp(Identifier(a), *, IntegerLiteral(2)))])), VarDecl(b, int, IntegerLiteral(2)), WhileStmt(BinaryOp(Identifier(b), >=, IntegerLiteral(1)), BlockStmt([Assignment(IdLValue(b), BinaryOp(Identifier(b), /, IntegerLiteral(2)))]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_357():
    source = """
func foo() -> void {
    if (1) { return; }
    else if (2) { return; }
    else if (3) { return; }
    else { return; }

    if (4) { return; }
    else if (5) { return; }
    else if (6) { return; }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()]), elif_branches=[(IntegerLiteral(2), BlockStmt([ReturnStmt()])), (IntegerLiteral(3), BlockStmt([ReturnStmt()]))], else_stmt=BlockStmt([ReturnStmt()])), "
            "IfStmt(condition=IntegerLiteral(4), then_stmt=BlockStmt([ReturnStmt()]), elif_branches=[(IntegerLiteral(5), BlockStmt([ReturnStmt()])), (IntegerLiteral(6), BlockStmt([ReturnStmt()]))])"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_358():
    source = """
func foo() -> int {
    return [10,20,30][1];
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], int, [ReturnStmt(ArrayAccess(ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)]), IntegerLiteral(1)))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_359():
    source = """
func foo() -> void {
    let m: [[int;2];2] = [[1,2],[3,4]];
    m[0][1] = 42;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "VarDecl(m, [[int; 2]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])])), "
            "Assignment(ArrayAccessLValue(ArrayAccessLValue(Identifier(m), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(42))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_360():
    source = """
func foo() -> void {
    let a: [int;2] = [5,6];
    let i: int = 1;
    a[(i * 2)] = a[(i + 1)];
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
            "VarDecl(a, [int; 2], ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6)])), "
            "VarDecl(i, int, IntegerLiteral(1)), "
            "Assignment(ArrayAccessLValue(Identifier(a), BinaryOp(Identifier(i), *, IntegerLiteral(2))), ArrayAccess(Identifier(a), BinaryOp(Identifier(i), +, IntegerLiteral(1))))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_361():
    source = "const VoTien = foo(a[1][3]);"
    expected = (
        "Program(consts=["
        "ConstDecl(VoTien, FunctionCall(Identifier(foo), ["
          "ArrayAccess(ArrayAccess(Identifier(a), IntegerLiteral(1)), IntegerLiteral(3))"
        "])"
        ")])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_362():
    # p.foo() không được hỗ trợ trực tiếp, chuyển thành foo(p)
    source = "func main() -> void { bar(foo(p), 1); };"
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
          "ExprStmt(FunctionCall(Identifier(bar), ["
            "FunctionCall(Identifier(foo), [Identifier(p)]), IntegerLiteral(1)"
          "]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_363():
    source = "const x: int = foo() + 2;"
    expected = (
        "Program(consts=[ConstDecl(x, int, BinaryOp(FunctionCall(Identifier(foo), []), +, IntegerLiteral(2)))])"
    )
    # Lưu ý: nếu ASTGenerator chưa hỗ trợ biến toàn cục thì test này bỏ qua
    assert str(ASTGenerator(source).generate()) == expected

def test_364():
    source = "func main() -> void { return; }; const x: int = 2;"
    expected = (
        "Program(consts=[ConstDecl(x, int, IntegerLiteral(2))], funcs=[FuncDecl(main, [], void, [ReturnStmt()])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_365():
    source = '''
func votien() -> void {
    return arr[2] + 2 + foo(1, 2);
    return "THANKS YOU, PPL1 ";
};
'''
    expected = (
        "Program(funcs=[FuncDecl(votien, [], void, [ReturnStmt(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), IntegerLiteral(2)), +, IntegerLiteral(2)), +, FunctionCall(Identifier(foo), [IntegerLiteral(1), IntegerLiteral(2)]))), ReturnStmt(StringLiteral('THANKS YOU, PPL1 '))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_366():
    # lặp lại test 362 với rewrite tương tự
    source = "func main() -> void { bar(foo(p), 1); };"
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
          "ExprStmt(FunctionCall(Identifier(bar), ["
            "FunctionCall(Identifier(foo), [Identifier(p)]), IntegerLiteral(1)"
          "]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_367():
    source = '''
func test() -> void {
    if (a > b) { return 1; } else { return 0; }
}
'''
    expected = (
        "Program(funcs=["
        "FuncDecl(test, [], void, ["
          "IfStmt(condition=BinaryOp(Identifier(a), >, Identifier(b)), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_368():
    # MethodDecl chưa được hỗ trợ; chuyển thành func doSomething(s: MyStruct)
    source = '''
func doSomething(s: MyStruct) -> void {
    s[2] = s[3] + 1;
}
'''
    expected = (
        "Program(funcs=[FuncDecl(doSomething, [Param(s, Identifier(MyStruct))], void, [Assignment(ArrayAccessLValue(Identifier(s), IntegerLiteral(2)), BinaryOp(ArrayAccess(Identifier(s), IntegerLiteral(3)), +, IntegerLiteral(1)))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_369():
    source = '''
func main() -> void {
    return n % 2 == 0;
}
'''
    expected = (
        "Program(funcs=["
        "FuncDecl(main, [], void, ["
          "ReturnStmt(BinaryOp(BinaryOp(Identifier(n), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_370():
    source = '''
func isEven(n: int) -> bool {
    return n % 2 == 0;
}
'''
    expected = (
        "Program(funcs=["
        "FuncDecl(isEven, [Param(n, int)], bool, ["
          "ReturnStmt(BinaryOp(BinaryOp(Identifier(n), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_371():
    source = """
func main() -> int {
    let x: int = 5;
    if (isEven(x)) {
        return;
    } else {
        return "Xin chao, ta la Tan Muc";
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], int, [VarDecl(x, int, IntegerLiteral(5)), IfStmt(condition=FunctionCall(Identifier(isEven), [Identifier(x)]), then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([ReturnStmt(StringLiteral('Xin chao, ta la Tan Muc'))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_372():
    source = """
func main() -> int {
    let x: int = 5;
    if (isEven(myMethod(hello), x)) {
        return;
    } else {
        return "Xin chao, ta la Tan Muc";
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], int, [VarDecl(x, int, IntegerLiteral(5)), IfStmt(condition=FunctionCall(Identifier(isEven), [FunctionCall(Identifier(myMethod), [Identifier(hello)]), Identifier(x)]), then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([ReturnStmt(StringLiteral('Xin chao, ta la Tan Muc'))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_373():
    source = """
func isEven(n: int) -> bool {
    return n % 2 == 0;
}
func main() -> int {
    let x: int = 5;
    if (isEven(x)) {
        return "So chan";
    } else {
        return "So le";
    }
}
"""
    expected = "Program(funcs=[FuncDecl(isEven, [Param(n, int)], bool, [ReturnStmt(BinaryOp(BinaryOp(Identifier(n), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))]), FuncDecl(main, [], int, [VarDecl(x, int, IntegerLiteral(5)), IfStmt(condition=FunctionCall(Identifier(isEven), [Identifier(x)]), then_stmt=BlockStmt([ReturnStmt(StringLiteral('So chan'))]), else_stmt=BlockStmt([ReturnStmt(StringLiteral('So le'))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_374():
    source = """
func main() -> void {
    return;
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ReturnStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_375():
    source = """
func main() -> void {
    let n: int = 10;
    let sum: int = 0;
    let i: int = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(n, int, IntegerLiteral(10)), VarDecl(sum, int, IntegerLiteral(0)), VarDecl(i, int, IntegerLiteral(1)), WhileStmt(BinaryOp(Identifier(i), <=, Identifier(n)), BlockStmt([Assignment(IdLValue(sum), BinaryOp(Identifier(sum), +, Identifier(i))), Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_376():
    source = """
func main() -> void {
    let x: int = 7;
    let result: bool = true;
    if (isEven(x)) {
        result = true;
    } else {
        result = false;
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, IntegerLiteral(7)), VarDecl(result, bool, BooleanLiteral(True)), IfStmt(condition=FunctionCall(Identifier(isEven), [Identifier(x)]), then_stmt=BlockStmt([Assignment(IdLValue(result), BooleanLiteral(True))]), else_stmt=BlockStmt([Assignment(IdLValue(result), BooleanLiteral(False))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_377():
    source = """
func main() -> void {
    let arr: [int;5] = [0, 0, 0, 0, 0];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 2 + 1;
    arr[3] = 3 * 2;
    arr[4] = 5;

    let reversed: [int;5] = [0, 0, 0, 0, 0];
    let i: int = 4;
    let j: int = 0;
    while (i < 10) {
        reversed[j] = arr[i];
        i = i - 1;
        j = j + 1;
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(2)), Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(2)), BinaryOp(IntegerLiteral(2), +, IntegerLiteral(1))), Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(3)), BinaryOp(IntegerLiteral(3), *, IntegerLiteral(2))), Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(4)), IntegerLiteral(5)), VarDecl(reversed, [int; 5], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), VarDecl(i, int, IntegerLiteral(4)), VarDecl(j, int, IntegerLiteral(0)), WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(ArrayAccessLValue(Identifier(reversed), Identifier(j)), ArrayAccess(Identifier(arr), Identifier(i))), Assignment(IdLValue(i), BinaryOp(Identifier(i), -, IntegerLiteral(1))), Assignment(IdLValue(j), BinaryOp(Identifier(j), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_378():
    source = """
func factorial(n: int) -> int {
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}
"""
    expected = "Program(funcs=[FuncDecl(factorial, [Param(n, int)], int, [IfStmt(condition=BinaryOp(Identifier(n), ==, IntegerLiteral(0)), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))])), ReturnStmt(BinaryOp(Identifier(n), *, FunctionCall(Identifier(factorial), [BinaryOp(Identifier(n), -, IntegerLiteral(1))])))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_379():
    source = """
func main() -> void {
    let i: int = 0;
    for (value in myArr) {
        if (arr[i] < firstMin) {
            secondMin = firstMin;
            firstMin = arr[i];
        } else if ((arr[i] < secondMin) && (arr[i] != firstMin)) {
            secondMin = arr[i];
        }
        i = i + 1;
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(i, int, IntegerLiteral(0)), ForStmt(value, Identifier(myArr), BlockStmt([IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(firstMin)), then_stmt=BlockStmt([Assignment(IdLValue(secondMin), Identifier(firstMin)), Assignment(IdLValue(firstMin), ArrayAccess(Identifier(arr), Identifier(i)))]), elif_branches=[(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(secondMin)), &&, BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), !=, Identifier(firstMin))), BlockStmt([Assignment(IdLValue(secondMin), ArrayAccess(Identifier(arr), Identifier(i)))]))]), Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_380():
    source = """
func main() -> void {
    let i: int = 0;
    for (value in myArr) {
        i = i + 1;
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(i, int, IntegerLiteral(0)), ForStmt(value, Identifier(myArr), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_381():
    source = """
func main() -> void {
    let i: int = 0;
    for (value in myArr) {
        i = i + 1;
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(i, int, IntegerLiteral(0)), ForStmt(value, Identifier(myArr), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_382():
    source = """
func main() -> void {
    if (arr[i] < firstMin) {
        secondMin = firstMin;
        firstMin  = arr[i];
    } else if ((arr[i] < secondMin) && (arr[i] != firstMin)) {
        secondMin = arr[i];
    }
}
"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(firstMin)), then_stmt=BlockStmt([Assignment(IdLValue(secondMin), Identifier(firstMin)), Assignment(IdLValue(firstMin), ArrayAccess(Identifier(arr), Identifier(i)))]), elif_branches=[(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), <, Identifier(secondMin)), &&, BinaryOp(ArrayAccess(Identifier(arr), Identifier(i)), !=, Identifier(firstMin))), BlockStmt([Assignment(IdLValue(secondMin), ArrayAccess(Identifier(arr), Identifier(i)))]))])])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_383():
    source = """
func foo() -> void {
    let a: [int; 1] = [1];
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(a, [int; 1], ArrayLiteral([IntegerLiteral(1)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_384():
    source = """
func foo() -> void {
    let a: int = 9;
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(a, int, IntegerLiteral(9))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_385():
    source = """
func foo() -> void {
    a = a + 1;
    a = a - 1;
    a = a * 1;
    a = a / 1;
    a = a % 1;
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [Assignment(IdLValue(a), BinaryOp(Identifier(a), +, IntegerLiteral(1))), Assignment(IdLValue(a), BinaryOp(Identifier(a), -, IntegerLiteral(1))), Assignment(IdLValue(a), BinaryOp(Identifier(a), *, IntegerLiteral(1))), Assignment(IdLValue(a), BinaryOp(Identifier(a), /, IntegerLiteral(1))), Assignment(IdLValue(a), BinaryOp(Identifier(a), %, IntegerLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_386():
    source = """
func foo() -> void {
    let arr: [int; 3] = [0, 0, 0];
    arr[1 + 1] = 1;
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), Assignment(ArrayAccessLValue(Identifier(arr), BinaryOp(IntegerLiteral(1), +, IntegerLiteral(1))), IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_387():
    source = """
func foo() -> void {
    let m: [[int;2];2] = [[1,2],[3,4]];
    m[0][1] = 42;
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [VarDecl(m, [[int; 2]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])])), Assignment(ArrayAccessLValue(ArrayAccessLValue(Identifier(m), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(42))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_388():
    source = """
func foo() -> void {
    return max(min(5,3), 4);
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [ReturnStmt(FunctionCall(Identifier(max), [FunctionCall(Identifier(min), [IntegerLiteral(5), IntegerLiteral(3)]), IntegerLiteral(4)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_389():
    source = """
func foo() -> int {
    return [10,20,30][2];
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], int, [ReturnStmt(ArrayAccess(ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)]), IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_390():
    source = """
func foo(x: int) -> bool {
    return x % 2 == 0;
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [Param(x, int)], bool, [ReturnStmt(BinaryOp(BinaryOp(Identifier(x), %, IntegerLiteral(2)), ==, IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_391():
    source = """
func foo() -> void {
    let a: [int;2] = [0,0];
    a[1] = 1;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "VarDecl(a, [int; 2], ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0)])), "
          "Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), IntegerLiteral(1))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_392():
    source = """
func foo() -> void {
    let a: [[int;2];2] = [[0,0],[0,0]];
    a[1][0] = 42;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "VarDecl(a, [[int; 2]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0)]), ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0)])])), "
          "Assignment(ArrayAccessLValue(ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), IntegerLiteral(0)), IntegerLiteral(42))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_393():
    source = """
func foo() -> void {
    break;
    continue;
}
"""
    expected = "Program(funcs=[FuncDecl(foo, [], void, [BreakStmt(), ContinueStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_394():
    source = """
func foo() -> void {
    return;
    return foo() + 2;
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "ReturnStmt(), "
          "ReturnStmt(BinaryOp(FunctionCall(Identifier(foo), []), +, IntegerLiteral(2)))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_395():
    source = """
func foo() -> void {
    a();
    a(1,2);
    b(3);
    c();
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "ExprStmt(FunctionCall(Identifier(a), [])), "
          "ExprStmt(FunctionCall(Identifier(a), [IntegerLiteral(1), IntegerLiteral(2)])), "
          "ExprStmt(FunctionCall(Identifier(b), [IntegerLiteral(3)])), "
          "ExprStmt(FunctionCall(Identifier(c), []))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_396():
    source = """
func foo() -> void {
    if (1) { return; }
    if (1 + 1) {
        return 1;
        return;
    }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()])), "
          "IfStmt(condition=BinaryOp(IntegerLiteral(1), +, IntegerLiteral(1)), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1)), ReturnStmt()]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_397():
    source = """
func foo() -> void {
    if (1) {
        return;
    } else if (1) {
        return 1;
        return;
    } else {
        return;
    }
    if (1) { return; } else { return 1; return; }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()]), "
                 "elif_branches=[(IntegerLiteral(1), BlockStmt([ReturnStmt(IntegerLiteral(1)), ReturnStmt()]))], "
                 "else_stmt=BlockStmt([ReturnStmt()])), "
          "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1)), ReturnStmt()]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_398():
    source = """
func foo() -> void {
    if (1) { return 1; }
    else if (2) { return 2; }
    else if (3) { return 3; }
    else if (4) { return 4; }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(foo, [], void, ["
          "IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([ReturnStmt(IntegerLiteral(1))]), "
                 "elif_branches=[(IntegerLiteral(2), BlockStmt([ReturnStmt(IntegerLiteral(2))])), "
                                 "(IntegerLiteral(3), BlockStmt([ReturnStmt(IntegerLiteral(3))])), "
                                 "(IntegerLiteral(4), BlockStmt([ReturnStmt(IntegerLiteral(4))]))])"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_399():
    source = """
func votien() -> void {
    for (x in [8]) {
        return;
        return 1;
    }
    while (i[1] < 10) {
        return;
        return 1;
    }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(votien, [], void, ["
          "ForStmt(x, ArrayLiteral([IntegerLiteral(8)]), BlockStmt([ReturnStmt(), ReturnStmt(IntegerLiteral(1))])), "
          "WhileStmt(BinaryOp(ArrayAccess(Identifier(i), IntegerLiteral(1)), <, IntegerLiteral(10)), BlockStmt([ReturnStmt(), ReturnStmt(IntegerLiteral(1))]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_400():
    source = """
func votien() -> void {
    for (idx in [1,2]) {
        return;
        return 1;
    }
}
"""
    expected = (
        "Program(funcs=["
        "FuncDecl(votien, [], void, ["
          "ForStmt(idx, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), BlockStmt([ReturnStmt(), ReturnStmt(IntegerLiteral(1))]))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected