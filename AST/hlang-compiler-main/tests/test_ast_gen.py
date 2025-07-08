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
