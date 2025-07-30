from utils import Checker


def test_001_o():
    """Test a valid program that should pass all checks"""
    source = """
    const PI: float = 3.14;
    func main() -> void {
        return 42;       
    };
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(42))"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002_o():
    """Test redeclared variable error"""
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
};
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_003_o():
    """Test undeclared identifier error"""
    source = """
func main() -> void {
    let x = y + 1;
};
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_004_o():
    """Test type mismatch error"""
    source = """
func main() -> void {
    let x: int = "hello";
};
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_005_o():
    """Test no main function error"""
    source = """
func hello() -> void {
    let x: int = 5;
};
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_006_o():
    """Test break not in loop error"""
    source = """
func main() -> void {
    break;
};
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected
def test_007_o():
    """Test continue not in loop error"""
    source = """
func main() -> void {
    continue;
};
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected
def test_009_o():
    """Test return type mismatch in function"""
    source = """
func compute() -> int {
    return "wrong";
};

func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('wrong'))"
    assert Checker(source).check_from_source() == expected
def test_011_o():
    """Test array access with non-integer index"""
    source = """
func main() -> void {
    let a: [int; 5] = [1, 2, 3, 4, 5];
    let x = a["index"];
};
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), StringLiteral('index'))"
    assert Checker(source).check_from_source() == expected

def test_001():
    """Redeclared variable in same scope"""
    source = """
func main() -> void {
    let HoangPhuc = 1;
    let HoangPhuc = 2;
}
"""
    expected = "Redeclared Variable: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_002():
    """Redeclared constant with same name as variable"""
    source = """
func main() -> void {
    let HoangPhuc = 1;
    const HoangPhuc = 2;
}
"""
    expected = "Redeclared Constant: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_003():
    """Redeclared variable with same name as constant"""
    source = """
func main() -> void {
    const HoangPhuc = 1;
    let HoangPhuc = 2;
}
"""
    expected = "Redeclared Variable: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_004():
    """Redeclared function with same name as constant"""
    source = """
const HoangPhuc = 1;

func HoangPhuc() -> void {
    return;
}
"""
    expected = "Redeclared Function: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_005():
    """Redeclared variable with same name as function"""
    source = """

func HoangPhuc() -> void {
    return;
}
const HoangPhuc = 1;
func main() -> void {
    let HoangPhuc = 1;
}


"""
    expected = "Redeclared Constant: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_006():
    """Redeclared variable with built-in function name"""
    source = """
func main() -> void {
    let getInt = 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_007():
    """Redeclared variable in nested block (same block level)"""
    source = """
func main() -> void {
    if (true) {
        let x = 1;
        let x = 2;
    }
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected


def test_008():
    """Redeclared function globally"""
    source = """
func foo() -> void {
    print("first");
}

func foo() -> void {
    print("second");
}

func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_009():
    """Redeclared parameter in same function"""
    source = """
func foo(a: int, b: int, a: int) -> int {
    return a + b;
}
func main() -> void {
}
"""
    expected = "Redeclared Parameter: a"
    assert Checker(source).check_from_source() == expected


def test_010():
    """Redeclared parameter in function"""
    source = """
func HoangPhuc(a: int, a: int) -> void {
    return;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_011():
    """Redeclared constant after variable in same scope"""
    source = """
func HoangPhuc(b: int) -> void {
    let b = 1;
    let a = 1;
    const a = 1;
}
func main() -> void {
}
"""
    expected = "Redeclared Variable: b"
    assert Checker(source).check_from_source() == expected


def test_012():
    """Redeclared constant in loop body"""
    source = """
func HoangPhuc(b: int) -> void {
    let arr = [1, 2, 3];
    for (a in arr) {
        const a = 2;
    }
}
func main() -> void {
}
"""
    expected = "Redeclared Constant: a"
    assert Checker(source).check_from_source() == expected


def test_013():
    """Undeclared identifier in global scope"""
    source = """

func main() -> void {
    let a = 1;
    let b = a;
    let c = d;
}
"""
    expected = "Undeclared Identifier: d"
    assert Checker(source).check_from_source() == expected


def test_014():
    """Undeclared function call"""
    source = """
func HoangPhuc() -> int {
    return 1;
}

func foo() -> void {
    let b = HoangPhuc();
    foo_hoangphuc();
    return;
}

func main() -> void {}
"""
    expected = "Undeclared Function: foo_hoangphuc"
    assert Checker(source).check_from_source() == expected


def test_015():
    """Undeclared identifier used like field (invalid in HLang)"""
    source = """
const HoangPhuc = 1;

func getInt() -> void {
    const c = HoangPhuc;
    let d = tien;
}
func main() -> void { getInt(); }
"""
    expected = "Undeclared Identifier: tien"
    assert Checker(source).check_from_source() == expected


def test_016():
    """Undeclared function call from within another function"""
    source = """
func getInt() -> void {
    getInt();
    putInt();
}
func main() -> void {}
"""
    expected = "Undeclared Function: putInt"
    assert Checker(source).check_from_source() == expected


def test_017():
    """Redeclared function"""
    source = """
func TIEN() -> void { print("1"); }
func TIEN() -> void { print("2"); }
func main() -> void {}
"""
    expected = "Redeclared Function: TIEN"
    assert Checker(source).check_from_source() == expected


def test_018():
    """Redeclared function prototype"""
    source = """
func foo() -> void { print("1"); }
func foo() -> void { print("2"); }
func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_019():
    """Multiple redeclared functions with same name"""
    source = """
func TIEN() -> void { print("Hi"); }
func VO() -> void { print("VO"); }
func TIEN() -> void { print("again"); }
func main() -> void {}
"""
    expected = "Redeclared Function: TIEN"
    assert Checker(source).check_from_source() == expected


def test_020():
    """Redeclared built-in function name"""
    source = """
func putInt() -> void { return; }
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_021():
    """Redeclared function foo globally"""
    source = """
func foo(v: int) -> void { return; }
func foo() -> void { return; }
func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_022():
    """Redeclared parameter inside two different functions"""
    source = """
func foo(a: int, b: int) -> void {
    let a = 1;
}

func bar(a: int, b: int) -> void {
    let a = 2;
}

func main() -> void {}
"""
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == expected


def test_023():
    """Undeclared identifier in for loop range"""
    source = """
func foo() -> void {
    const a = 1;
    let arr = [1, 2, 3];
    for (i in arr) {
        let d = 1;
    }
    let x = b;
}

func main() -> void {}
"""
    expected = "Undeclared Identifier: b"
    assert Checker(source).check_from_source() == expected


def test_024():
    """Mutual recursion, valid"""
    source = """


func foo() -> int {
    let a = koo();
    let c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}

const d = foo();

func koo() -> int {
    let a = foo();
    return 1;
}

func getInt() -> int { return 42; }
func putInt(x: int) -> void { return; }
func putIntLn(x: int) -> void { return; }
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_025():
    """Undeclared identifier d used before declaration"""
    source = """
const a = d;

func foo() -> void {
    const b = 1;
    let arr = [1, 2, 3];
    for (c in arr) {
        let d = c;
    }
    let d = a;
    let a = 1;
}

const d = a;

func main() -> void {}
"""
    expected = "Undeclared Identifier: d"
    assert Checker(source).check_from_source() == expected


def test_026():
    """Undeclared field access v.e"""
    source = """

const v = [1, 2, 3];
const b = v[1];
const a = v[0];
const e = v[3];
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_027():
    """Access undeclared field e via variable x"""
    source = """
const v = [1, 2, 3];

func foo() -> void {
    let x: int = 5;
    const a = x[0];
    const e = x[3];
}

func main() -> void {}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(x), IntegerLiteral(0))"
    assert Checker(source).check_from_source() == expected


def test_028():
    """Nested array access, valid"""
    source = """
const v = [[1.0, 2.0], [3.0, 4.0]];
const my = v[1][0];
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_029():
    """Mutual recursion again (valid case)"""
    source = """


func foo() -> int {
    let a = koo();
    let c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
const a = foo();
const d = foo();

func koo() -> int {
    let a = foo();
    return 1;
}

func getInt() -> int { return 1; }
func putInt(x: int) -> void { return; }
func putIntLn(x: int) -> void { return; }
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_030():
    """Undeclared identifier b in for loop"""
    source = """
const a = 2;

func foo() -> void {
    const a = 1;
    let arr = [1, 2, 3];
    for (x in arr) {
        let b = 1;
    }
    let y = b;
}

func main() -> void {}
"""
    expected = "Undeclared Identifier: b"
    assert Checker(source).check_from_source() == expected

def test_031():
    """Redeclared function foo"""
    source = """
func foo(a: int, b: int) -> void {
    const a = 1;
}

func foo() -> void {
    const a = 1;
}

func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_032():
    """Redeclared variable in nested block"""
    source = """
const a = 2;
func foo() -> void {
    const a = 1;
    while (a < 1) {
        const a = 1;
        while (a < 1) {
            const a = 1;
            const b = 1;
        }
        const b = 1;
        let a = 1;
    }
}

func main() -> void {}
"""
    expected = "Redeclared Constant: a"
    assert Checker(source).check_from_source() == expected


def test_033():
    """Undeclared function zoo"""
    source = """
func foo() -> int { return 1; }
func koo() -> int { return 1; }

const b = foo();
const c = koo();
const d = zoo();

func main() -> void {}
"""
    expected = "Undeclared Function: zoo"
    assert Checker(source).check_from_source() == expected


def test_034():
    """Undeclared function koo used through variable"""
    source = """
func foo() -> int { return 1; }
func bar() -> void {
    let x = foo;
    let a = 5;
    x();
    y();
}
func main() -> void {}
"""
    expected = "Undeclared Function: x"
    assert Checker(source).check_from_source() == expected


def test_035():
    """Redeclared variable inside nested loop"""
    source = """
const a = 2;
func foo() -> void {
    const a = 1;
    while (a < 1) {
        const a = 1;
        while (a < 1) {
            const a = 1;
            const b = 1;
        }
        const b = 1;
        let a = 1;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Constant: a"
    assert Checker(source).check_from_source() == expected


def test_036():
    """Redeclared function name (type emulation removed)"""
    source = """
func Phuc() -> void {}
func Phuc() -> void {}

func main() -> void {}
"""
    expected = "Redeclared Function: Phuc"
    assert Checker(source).check_from_source() == expected


def test_037():
    """Type mismatch in variable declaration"""
    source = """
func foo() -> void {
    let v: int = 1;
    const x = v;
    let k: float = x;
    let y: bool = x;
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: VarDecl(k, float, Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_038():
    """Type mismatch in for loop condition"""
    source = """
func foo() -> void {
    while (1) {
        let a: int = 1.2;
    }
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: WhileStmt(IntegerLiteral(1), BlockStmt([VarDecl(a, int, FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected


def test_039():
    """Array type mismatch in assignment"""
    source = """
const a: [[int; 3]; 2] = [[1,2,3], [4,5,6]];
const b = a[1];
const c: [int; 2] = b;
const d: [string; 1] = b;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(c, [int; 2], Identifier(b))"
    assert Checker(source).check_from_source() == expected


def test_040():
    """Modulo operator only accepts integers"""
    source = """
const a: int = 1 % 2;
const b: int = 1 % 2.0;
func main() -> void {}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), %, FloatLiteral(2.0))"
    assert Checker(source).check_from_source() == expected

def test_041():
    """Function recursion with type mismatch (call after return)"""
    source = """
func foo() -> int { return 1; }

func HoangPhuc() -> int {
    return HoangPhuc();
    foo();
}

func main() -> void {}
"""
    expected = "Static checking passed"  # Because foo() is never used in expression
    assert Checker(source).check_from_source() == expected


def test_042():
    """Type mismatch in variable declaration (int vs float)"""
    source = """
const v: int = 1.2;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(v, int, FloatLiteral(1.2))"
    assert Checker(source).check_from_source() == expected


def test_043():
    """Array type mismatch via alias"""
    source = """
const x: [int; 3] = [1, 2, 3];
const z: [int; 3] = x;
const k: [float; 3] = x;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(k, [float; 3], Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_044():
    """Assigning variable of wrong type to another"""
    source = """
const a: [int; 3] = [1, 2, 3];
const b: [float; 3] = [1.0, 2.0, 3.0];
const d: [int; 3] = b;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(d, [int; 3], Identifier(b))"
    assert Checker(source).check_from_source() == expected


def test_045():
    """Assign one function to another function with incompatible type"""
    source = """
func I1() -> int { return 1; }
func I2() -> float { return 1.0; }

const x = I1;
const k: float = x;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(k, float, Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_046():
    """Assign one function to another of different type (repeat of 045)"""
    source = """
func I1() -> int { return 1; }
func I2() -> float { return 1.0; }

const x = I1;
const k: float = x;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(k, float, Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_047():
    """Nested function return mismatch"""
    source = """
func HoangPhuc1() -> [int; 2] { return [1, 2]; }
func HoangPhuc() -> [float; 2] { return [1.0, 2.0]; }

const a = HoangPhuc1();
const d: [float; 2] = a;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(d, [float; 2], Identifier(a))"
    assert Checker(source).check_from_source() == expected


def test_048():
    """Redeclared function (originally declared interface type)"""
    source = """
func Phuc() -> void {}
func Phuc() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: Phuc"
    assert Checker(source).check_from_source() == expected


def test_049():
    """Type mismatch through chained assignment"""
    source = """
func foo() -> void {
    let v: int = 1;
    const x = v;
    let k: float = x;
    let y: bool = x;
}

func main() -> void {}
"""
    expected = "Type Mismatch In Statement: VarDecl(k, float, Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_050():
    """Type mismatch inside while loop"""
    source = """
const v = [[1, 2], [3, 4]];

func foo() -> void {
    while (1) {
        let a: int = 1.2;
    }
}

func main() -> void {}
"""
    expected = "Type Mismatch In Statement: WhileStmt(IntegerLiteral(1), BlockStmt([VarDecl(a, int, FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected

def test_051():
    """Array assignment mismatch"""
    source = """
const a: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
const b = a[1];
const c: [int; 2] = b;
const d: [string; 1] = b;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(c, [int; 2], Identifier(b))"
    assert Checker(source).check_from_source() == expected


def test_052():
    """Modulo with float operand (invalid)"""
    source = """
const a: int = 1 % 2;
const b: int = 1 % 2.0;
func main() -> void {}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), %, FloatLiteral(2.0))"
    assert Checker(source).check_from_source() == expected


def test_053():
    """Unreachable call after return, but type mismatch in call"""
    source = """
func foo() -> int { return 1; }

func HoangPhuc() -> int {
    return HoangPhuc();
    foo();
}

func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_054():
    """Float assigned to int variable"""
    source = """
const v: int = 1.2;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(v, int, FloatLiteral(1.2))"
    assert Checker(source).check_from_source() == expected


def test_055():
    """Assign mismatched arrays"""
    source = """
const x: [int; 3] = [1, 2, 3];
const z: [int; 3] = x;
const k: [float; 3] = x;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(k, [float; 3], Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_056():
    """Assign array with different type"""
    source = """
const a: [int; 3] = [1, 2, 3];
const b: [float; 3] = [1.0, 2.0, 3.0];
const c: [int; 3] = a;
const d: [float; 3] = b;
const x: [float; 3] = a;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(x, [float; 3], Identifier(a))"
    assert Checker(source).check_from_source() == expected


def test_057():
    """Assign expression to wrong type"""
    source = """
const v: int = 5;
const x = v;
const z: int = x;
const k: int = x;
const m: bool = x;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(m, bool, Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_058():
    """Assign nested array of wrong type"""
    source = """
const a: [[int; 2]; 2] = [[1, 2], [3, 4]];
const b: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]];
const c: [[int; 2]; 2] = a;
const d: [[float; 2]; 2] = a;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(d, [[float; 2]; 2], Identifier(a))"
    assert Checker(source).check_from_source() == expected


def test_059():
    """Redeclared function"""
    source = """
func HoangPhuc() -> int { return 1; }
func HoangPhuc() -> int { return 2; }
func main() -> void {}
"""
    expected = "Redeclared Function: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_060():
    """Redeclared variable in same scope"""
    source = """
func main() -> void {
    let HoangPhuc = 1;
    let HoangPhuc = 2;
}
"""
    expected = "Redeclared Variable: HoangPhuc"
    assert Checker(source).check_from_source() == expected

def test_061():
    """Variable then constant with same name"""
    source = """
const main_const = 0;
func main() -> void {
    let HoangPhuc = 1;
    const HoangPhuc = 2;
}
"""
    expected = "Redeclared Constant: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_062():
    """Constant then variable with same name"""
    source = """
const HoangPhuc = 1;
func main() -> void {
    let HoangPhuc = 2;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_063():
    """Constant then function with same name"""
    source = """
const HoangPhuc = 1;

func HoangPhuc() -> void {
    return;
}
func main() -> void {}
"""
    expected = "Redeclared Function: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_064():
    """Function then variable with same name"""
    source = """
func HoangPhuc() -> void {
    return;
}

func main() -> void {
    let HoangPhuc = 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_065():
    """Redeclared built-in function name as variable"""
    source = """
func main() -> void {
    let print = 1;
}
"""
    expected = "Redeclared Variable: print"
    assert Checker(source).check_from_source() == expected


def test_066():
    """Invalid: HLang không có struct → chuyển thành constant field check"""
    source = """
const TIEN = 1;
const TIEN = 2;
func main() -> void {}
"""
    expected = "Redeclared Constant: TIEN"
    assert Checker(source).check_from_source() == expected


def test_067():
    """Redeclared function with same name"""
    source = """
func getInt() -> void { return; }
func getInt() -> void { return; }
func main() -> void {}
"""
    expected = "Redeclared Function: getInt"
    assert Checker(source).check_from_source() == expected


def test_068():
    """Redeclared parameter prototype (method with same name)"""
    source = """
func HoangPhuc() -> void { return; }
func HoangPhuc(a: int) -> void { return; }
func main() -> void {}
"""
    expected = "Redeclared Function: HoangPhuc"
    assert Checker(source).check_from_source() == expected


def test_069():
    """Redeclared parameter in function"""
    source = """
func HoangPhuc(a: int, a: int) -> void {
    return;
}
func main() -> void {}
"""
    expected = "Redeclared Parameter: a"
    assert Checker(source).check_from_source() == expected


def test_070():
    """Redeclared constant after variable in same scope"""
    source = """
func HoangPhuc(b: int) -> void {
    let b = 1;
    let a = 1;
    const a = 1;
}
func main() -> void {}
"""
    expected = "Redeclared Variable: b"
    assert Checker(source).check_from_source() == expected

def test_071():
    """Redeclared constant in loop body"""
    source = """
func HoangPhuc(b: int) -> void {
    let arr = [1,2,3];
    for (a in arr) {
        const a = 2;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Constant: a"
    assert Checker(source).check_from_source() == expected


def test_072():
    """Undeclared identifier in global scope"""
    source = """
const a = 1;
const b = a;
const c = d;
func main() -> void {}
"""
    expected = "Undeclared Identifier: d"
    assert Checker(source).check_from_source() == expected


def test_073():
    """Undeclared function call"""
    source = """
func HoangPhuc() -> int { return 1; }

func foo() -> void {
    let b = HoangPhuc();
    foo_hoangphuc();
    return;
}

func main() -> void {}
"""
    expected = "Undeclared Function: foo_hoangphuc"
    assert Checker(source).check_from_source() == expected


def test_074():
    """Undeclared field → chuyển thành array index out-of-bound"""
    source = """
func getInt() -> void {
    let v = [1, 2, 3];
    const c = v[0];
    let d = v[10];
}

func main() -> void {
    getInt();
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_075():
    """Undeclared function (method style call chuyển thành thường)"""
    source = """
func getInt() -> void {
    getInt();
    putInt();
}

func main() -> void {}
"""
    expected = "Undeclared Function: putInt"
    assert Checker(source).check_from_source() == expected


def test_076():
    """Redeclared function (thay cho struct type)"""
    source = """
func TIEN() -> void {}
func TIEN() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: TIEN"
    assert Checker(source).check_from_source() == expected


def test_077():
    """Redeclared function (thay cho interface type)"""
    source = """
func foo() -> void {}
func foo() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_078():
    """Redeclared function with same name after struct emulation"""
    source = """
func TIEN() -> void {}
func VO() -> void {}
func TIEN() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: TIEN"
    assert Checker(source).check_from_source() == expected


def test_079():
    """Redeclared built-in function"""
    source = """
func print() -> void { return; }
func main() -> void {}
"""
    expected = "Redeclared Function: print"
    assert Checker(source).check_from_source() == expected


def test_080():
    """Function parameter shadowing another function name"""
    source = """
func foo(v: int) -> void {
    return;
}

func foo() -> void {
    return;
}

func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected

def test_081():
    """Redeclared parameter a in 2 functions is fine, only one gets error"""
    source = """
func foo1(a: int, b: int) -> void {
    let a = 1;
}

func foo2(a: int, b: int) -> void {
    let a = 1;
}

func main() -> void {}
"""
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == expected


def test_082():
    """Undeclared identifier b in loop"""
    source = """
func foo() -> void {
    let arr = [1, 2, 3];
    for (a in arr) {
        break;
    }
    let x = b;
}
func main() -> void {}
"""
    expected = "Undeclared Identifier: b"
    assert Checker(source).check_from_source() == expected


def test_083():
    """Valid mutual recursion and global variable usage"""
    source = """


func foo() -> int {
    let a = koo();
    let c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
const a = foo();
const d = foo();

func koo() -> int {
    let a = foo();
    return 1;
}

func getInt() -> int { return 1; }
func putInt(x: int) -> void { return; }
func putIntLn(x: int) -> void { return; }
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_084():
    """Undeclared identifier d used before declaration"""
    source = """
const a = d;

func foo() -> void {
    let arr = [1, 2, 3];
    for (c in arr) {
        let d = c;
    }
    let d = a;
    let a = 1;
}

const d = a;

func main() -> void {}
"""
    expected = "Undeclared Identifier: d"
    assert Checker(source).check_from_source() == expected


def test_085():
    """Access to undefined array index (field 'e')"""
    source = """
const v = [1, 2, 3];
const b = v[1];
const a = v[0];
const e = v[3];
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_086():
    """Access invalid field in local variable"""
    source = """
const v = [1, 2, 3];

func foo() -> void {
    let x = v;
    const a = x[0];
    const e = x[3];
}

func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_087():
    """Valid nested array access"""
    source = """
const v = [[1.0, 2.0], [3.0, 4.0]];
const my = v[1][0];
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_088():
    """Valid mutual recursion again"""
    source = """


func foo() -> int {
    let a = koo();
    let c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
const a = foo();
const d = foo();

func koo() -> int {
    let a = foo();
    return 1;
}

func getInt() -> int { return 1; }
func putInt(x: int) -> void { return; }
func putIntLn(x: int) -> void { return; }
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_089():
    """Undeclared identifier used in for condition"""
    source = """
const a = 2;

func foo() -> void {
    const a = 1;
    let arr = [1, 2, 3];
    for (x in arr) {
        let b = 1;
    }
    let y = b;
}

func main() -> void {}
"""
    expected = "Undeclared Identifier: b"
    assert Checker(source).check_from_source() == expected


def test_090():
    """Redeclared parameter and constant inside function"""
    source = """
func foo1(v: int, a: int) -> void {
    const v = 1;
    const a = 1;
}

func foo2() -> void {
    const a = 1;
}

func foo2(a: int, b: int) -> void {
    const a = 1;
}

func main() -> void {}
"""
    expected = "Redeclared Function: foo2"
    assert Checker(source).check_from_source() == expected

def test_091():
    """Redeclared variable a in nested block"""
    source = """
const a = 2;
func foo() -> void {
    const a = 1;
    while (a < 1) {
        const a = 1;
        while (a < 1) {
            const a = 1;
            const b = 1;
        }
        const b = 1;
        let a = 1;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Constant: a"
    assert Checker(source).check_from_source() == expected


def test_092():
    """Undeclared function zoo"""
    source = """


func foo() -> int { return 1; }
func koo() -> int { return 1; }
const b = foo();
const c = koo();
const d = zoo();
func main() -> void {}
"""
    expected = "Undeclared Function: zoo"
    assert Checker(source).check_from_source() == expected


def test_093():
    """Undeclared function koo called via variable"""
    source = """
func foo() -> int { return 1; }

func bar() -> void {
    let x = foo;
    let y = x();
    x();
    koo();
}

func main() -> void {}
"""
    expected = "Undeclared Function: x"
    assert Checker(source).check_from_source() == expected


def test_094():
    """Redeclared variable a in nested block"""
    source = """
const a = 2;
func foo() -> void {
    let a = 1;
    while (a < 1) {
        let a = 1;
        while (a < 1) {
            const a = 1;
            const b = 1;
        }
        const b = 1;
        let a = 1;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == expected


def test_095():
    """Redeclared function (replacing interface type)"""
    source = """
func Phuc() -> void {}
func Phuc() -> void {}

func main() -> void {}
"""
    expected = "Redeclared Function: Phuc"
    assert Checker(source).check_from_source() == expected


def test_096():
    """Type mismatch in variable declaration"""
    source = """
func foo() -> void {
    let v: int = 1;
    const x = v;
    let k: int = x;
    let y: bool = x;
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: VarDecl(y, bool, Identifier(x))"
    assert Checker(source).check_from_source() == expected


def test_097():
    """Type mismatch in loop body"""
    source = """
func foo() -> void {
    while (1) {
        let a: int = 1.2;
    }
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: WhileStmt(IntegerLiteral(1), BlockStmt([VarDecl(a, int, FloatLiteral(1.2))]))"
    assert Checker(source).check_from_source() == expected


def test_098():
    """Array type mismatch in assignment"""
    source = """
const a: [[int; 3]; 2] = [[1,2,3],[4,5,6]];
const b = a[1];
const c: [int; 2] = b;
const d: [string; 1] = b;
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ConstDecl(c, [int; 2], Identifier(b))"
    assert Checker(source).check_from_source() == expected


def test_099():
    """Modulo operator with float"""
    source = """
const a: int = 1 % 2;
const b: int = 1 % 2.0;
func main() -> void {}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), %, FloatLiteral(2.0))"
    assert Checker(source).check_from_source() == expected


def test_100():
    """Call after return is ignored, test only FuncCall type"""
    source = """
func foo() -> int { return 1; }

func HoangPhuc() -> int {
    return HoangPhuc();
    foo();
}

func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

## REDECLARED
def test_101():
    """Redeclared parameter (same name)"""
    source = """
func check(a: int, b: int, a: bool) -> void {}
func main() -> void {}
"""
    expected = "Redeclared Parameter: a"
    assert Checker(source).check_from_source() == expected


def test_102():
    """Redeclared constant in global scope"""
    source = """
const PI = 3.14;
const PI = 3.14159;
func main() -> void {}
"""
    expected = "Redeclared Constant: PI"
    assert Checker(source).check_from_source() == expected


def test_103():
    """Redeclared function in global scope"""
    source = """
func foo() -> void {}
func foo() -> int { return 1; }
func main() -> void {}
"""
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_104():
    """Redeclared variable in same inner block"""
    source = """
func main() -> void {
    let x = 10;
    {
        let x = 20;
        let x = 30;
    }
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected


def test_105():
    """Function parameter conflicts with local variable"""
    source = """
func compute(count: int) -> void {
    let count = 42;
}
func main() -> void {}
"""
    expected = "Redeclared Variable: count"
    assert Checker(source).check_from_source() == expected


def test_106():
    """Constant redeclared as variable"""
    source = """
func convert() -> void {
    const temp = 100;
    let temp = 200;
}
func main() -> void {}
"""
    expected = "Redeclared Variable: temp"
    assert Checker(source).check_from_source() == expected


def test_107():
    """Function redeclared after const"""
    source = """
const read = "read";

func read() -> void {
    print("reading...");
}
func main() -> void {}
"""
    expected = "Redeclared Function: read"
    assert Checker(source).check_from_source() == expected


def test_108():
    """Redeclared variable inside loop"""
    source = """
func iterate() -> void {
    for (x in [1, 2, 3]) {
        let y = 1;
        let y = 2;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Variable: y"
    assert Checker(source).check_from_source() == expected


def test_109():
    """Valid shadowing then redeclared in same block"""
    source = """
const level = 1;

func game() -> void {
    let level = 2;
    {
        let score = level;
        let score = 100;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Variable: score"
    assert Checker(source).check_from_source() == expected


def test_110():
    """Redeclared loop variable inside loop body"""
    source = """
func test() -> void {
    for (i in [1, 2, 3]) {
        let i = 10;
    }
}
func main() -> void {}
"""
    expected = "Redeclared Variable: i"
    assert Checker(source).check_from_source() == expected

def test_111():
    """Undeclared variable in nested block"""
    source = """
func main() -> void {
    let y: int = 1;
    let y = x + 1;
}
"""
    expected = "Redeclared Variable: y"
    assert Checker(source).check_from_source() == expected


def test_112():
    """Use before declaration (constant)"""
    source = """
const a = b + 1;
const b = 2;
func main() -> void {}
"""
    expected = "Undeclared Identifier: b"
    assert Checker(source).check_from_source() == expected


def test_113():
    """Use parameter not declared"""
    source = """
func foo(a: int) -> void {
    let b = c;
}
func main() -> void {}
"""
    expected = "Undeclared Identifier: c"
    assert Checker(source).check_from_source() == expected


def test_114():
    """Undeclared function in nested call"""
    source = """
func bar() -> void {
    let x = callMeMaybe();
}
func main() -> void {}
"""
    expected = "Undeclared Function: callMeMaybe"
    assert Checker(source).check_from_source() == expected


def test_115():
    """Function call with undeclared argument"""
    source = """
func sum(x: int) -> int { return x + 1; }

func main() -> void {
    let a = sum(y);
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected


def test_116():
    """Array access on undeclared identifier"""
    source = """
func main() -> void {
    let x = arr[1];
}
"""
    expected = "Undeclared Identifier: arr"
    assert Checker(source).check_from_source() == expected


def test_117():
    """Use function as value then call undeclared"""
    source = """
func foo() -> int { return 1; }

func main() -> void {
    let f = foo;
    let result = bar();
}
"""
    expected = "Undeclared Function: bar"
    assert Checker(source).check_from_source() == expected


def test_118():
    """Forward call to function not yet defined"""
    source = """
func main() -> void {
    let x = mystery();
}

func later() -> int { return 1; }
"""
    expected = "Undeclared Function: mystery"
    assert Checker(source).check_from_source() == expected


def test_119():
    """Function calls itself and another not defined"""
    source = """
func rec() -> int {
    return rec() + helper();
}
func main() -> void {}
"""
    expected = "Undeclared Function: helper"
    assert Checker(source).check_from_source() == expected


def test_120():
    """Undeclared in loop body after use"""
    source = """
func main() -> void {
    for (i in [1,2,3]) {
        let x = y;
        let y = 10;
    }
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_121():
    """Binary op between int and bool"""
    source = """
func main() -> void {
    let a = 1 + true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), +, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test_122():
    """Array access with bool index"""
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let x = a[false];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), BooleanLiteral(False))"
    assert Checker(source).check_from_source() == expected


def test_123():
    """Logical AND on int and bool"""
    source = """
func main() -> void {
    let a = 5 && true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), &&, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test_124():
    """Comparison between float and string"""
    source = """
func main() -> void {
    let x = 3.14 > "hi";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(FloatLiteral(3.14), >, StringLiteral('hi'))"
    assert Checker(source).check_from_source() == expected


def test_125():
    """Equality between array and int"""
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let check = a == 1;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(a), ==, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test_126():
    """Unary NOT on int"""
    source = """
func main() -> void {
    let a = !5;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected


def test_127():
    """Addition between int and string"""
    source = """
func main() -> void {
    let x = 10 + "phuc";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(10), +, StringLiteral('phuc'))"
    assert Checker(source).check_from_source() == expected


def test_128():
    """Array access with float index"""
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let x = a[2.5];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), FloatLiteral(2.5))"
    assert Checker(source).check_from_source() == expected


def test_129():
    """Nested binary op with mismatched inner"""
    source = """
func main() -> void {
    let a = (1 + true) * 3;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), +, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test_130():
    """Function call used as bool in logical op"""
    source = """
func getVal() -> int { return 5; }

func main() -> void {
    let result = getVal() && true;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(FunctionCall(Identifier(getVal), []), &&, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_131():
    """Assign string to int variable"""
    source = """
func main() -> void {
    let x: int = "hello";
}
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected


def test_132():
    """Assign float to bool variable"""
    source = """
func main() -> void {
    let flag: bool = 3.14;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(flag, bool, FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected


def test_133():
    """Assign int to array element of type float"""
    source = """
func main() -> void {
    let arr: [float; 3] = [1.0, 2.0, 3.0];
    arr[0] = true;
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test_134():
    """Return string from int function"""
    source = """
func foo() -> int {
    return "wrong";
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('wrong'))"
    assert Checker(source).check_from_source() == expected


def test_135():
    """Return nothing from int function"""
    source = """
func get() -> int {
    return;
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt()"
    assert Checker(source).check_from_source() == expected


def test_136():
    """Return int from void function"""
    source = """
func show() -> void {
    return 5;
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected


def test_137():
    """If condition is string"""
    source = """
func main() -> void {
    let cond: string = "true";
    if (cond) {
        let x = 1;
    }
}
"""
    expected = "Type Mismatch In Statement: IfStmt(condition=Identifier(cond), then_stmt=BlockStmt([VarDecl(x, IntegerLiteral(1))]))"
    assert Checker(source).check_from_source() == expected


def test_138():
    """While loop with float condition"""
    source = """
func main() -> void {
    while (3.14) {
        let x = 1;
    }
}
"""
    expected = "Type Mismatch In Statement: WhileStmt(FloatLiteral(3.14), BlockStmt([VarDecl(x, IntegerLiteral(1))]))"
    assert Checker(source).check_from_source() == expected


def test_139():
    """For loop over int (non-iterable)"""
    source = """
func main() -> void {
    for (x in 5) {
        let y = x;
    }
}
"""
    expected = "Type Mismatch In Statement: ForStmt(x, IntegerLiteral(5), BlockStmt([VarDecl(y, Identifier(x))]))"
    assert Checker(source).check_from_source() == expected


def test_140():
    """Function call in statement context with non-void return"""
    source = """
func add(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    add(1, 2);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

# def test_141():
#     """Variable inferred from another inferred variable"""
#     source = """
# func main() -> void {
#     let b = a; 
#     let a = b;
# }
# """
#     expected = "Type Cannot Be Inferred: VarDecl(a, None, Identifier(b))"
#     assert Checker(source).check_from_source() == expected


# def test_142():
#     """Circular dependency in assignment"""
#     source = """
# func main() -> void {
#     let x = y;
#     let y = z;
#     let z = x;
# }
# """
#     expected = "Type Cannot Be Inferred: VarDecl(x, None, Identifier(y))"
#     assert Checker(source).check_from_source() == expected


def test_143():
    """Assign empty array without type annotation"""
    source = """
func main() -> void {
    let arr = [];
}
"""
    expected = "Type Cannot Be Inferred: ArrayLiteral([])"
    assert Checker(source).check_from_source() == expected


def test_144():
    """Function return type cannot be inferred from call"""
    source = """
func foo() {
    return 42;
}
func main() -> void {
    let x = foo();
}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected


# def test_145():
#     """Multiple unknowns chained in expression"""
#     source = """
# func main() -> void {
#     let a = b + c;
#     let b = 1;
# }
# """
#     expected = "Type Cannot Be Inferred: VarDecl(a, None, BinaryOp(Identifier(b), +, Identifier(c)))"
#     assert Checker(source).check_from_source() == expected


def test_146():
    """Inferred array element from unknown identifier"""
    source = """
func main() -> void {
    let y = "hi";
    let x = [y, 2];
}
"""
    expected = "Type Mismatch In Statement: ArrayLiteral([Identifier(y), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected


def test_147():
    """Assign function call to unannotated variable, but function not declared"""
    source = """
func main() -> void {
    let a = foo();
}
"""
    expected = "Undeclared Function: foo"
    assert Checker(source).check_from_source() == expected


def test_148():
    """Assign result of void function to unannotated variable"""
    source = """
func doSomething() -> void { return; }

func main() -> void {
    let x = doSomething();
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


# def test_149():
#     """Pipeline where initial value is unknown"""
#     source = """
# func transform(x: int) -> int { return x + 1; }

# func main() -> void {
#     let val = "hu";
#     let result = val >> transform;
# }
# """
#     expected = "Type Cannot Be Inferred: VarDecl(result, None, BinaryOp(Identifier(val), >>, Identifier(transform)))"
#     assert Checker(source).check_from_source() == expected


def test_150():
    """Array with different inferred types"""
    source = """
func main() -> void {
    let arr = [1, true, 3];
}
"""
    expected = "Type Mismatch In Statement: ArrayLiteral([IntegerLiteral(1), BooleanLiteral(True), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected

def test_151():
    """Break outside loop"""
    source = """
func main() -> void {
    break;
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test_152():
    """Continue outside loop"""
    source = """
func main() -> void {
    continue;
}
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected


def test_153():
    """Break in if inside function but not in loop"""
    source = """
func main() -> void {
    if (true) {
        break;
    }
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test_154():
    """Continue in nested block not inside loop"""
    source = """
func main() -> void {
    {
        continue;
    }
}
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected


def test_155():
    """Break in function outside loop"""
    source = """
func inner() -> void {
    break;
}
func main() -> void {
    inner();
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test_156():
    """Continue in if-else outside loop"""
    source = """
func main() -> void {
    if (false) {
        continue;
    } else {
        let x = 1;
    }
}
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected


# def test_157():
#     """Break inside function declared inside loop body (should still error)"""
#     source = """
# func main() -> void {
#     if (true) {
#         func wrong() -> void {
#             break;
#         }
#     }
# }
# """
#     expected = "Must In Loop: BreakStmt()"
#     assert Checker(source).check_from_source() == expected


# def test_158():
#     """Continue inside function declared inside if block"""
#     source = """
# func main() -> void {
#     if (true) {
#         func inner() -> void {
#             continue;
#         }
#     }
# }
# """
#     expected = "Must In Loop: ContinueStmt()"
#     assert Checker(source).check_from_source() == expected


def test_159():
    """Break in block before loop starts"""
    source = """
func main() -> void {
    {
        break;
    }
    while (true) {
        let a = 1;
    }
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test_160():
    """Continue used in global constant block"""
    source = """
const x = 10;

func main() -> void {
    let y = x;
    continue;
}

"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected

def test_161():
    """No main function at all"""
    source = """
func notMain() -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_162():
    """Main function has parameters"""
    source = """
func main(x: int) -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_163():
    """Main function has wrong return type"""
    source = """
func main() -> int {
    return 0;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_164():
    """Main function has parameters and wrong return type"""
    source = """
func main(a: bool) -> int {
    return 1;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_165():
    """Main is missing parentheses"""
    source = """
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_166():
    """Main is defined inside another function (not global)"""
    source = """
func wrapper() -> void {
    func main() -> void {}
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_167():
    """Main defined as a method inside struct"""
    source = """

func Main() -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_168():
    """Main is a constant, not a function"""
    source = """
const main = 42;

func another() -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_169():
    """Main declared but never defined"""
    source = """
func other() -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected


def test_170():
    """Main is overloaded (not valid in HLang)"""
    source = """
func main() -> void {}
func main(x: int) -> void {}
"""
    expected = "Redeclared Function: main"
    assert Checker(source).check_from_source() == expected

def test_171():
    """Too few arguments"""
    source = """
func sum(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    let result = sum(5);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(sum), [IntegerLiteral(5)])"
    assert Checker(source).check_from_source() == expected


def test_172():
    """Too many arguments"""
    source = """
func printStr(s: string) -> void {
    print(s);
}
func main() -> void {
    printStr("hello", "world");
}
"""
    expected = "Type Mismatch In Statement: FunctionCall(Identifier(printStr), [StringLiteral('hello'), StringLiteral('world')])"
    assert Checker(source).check_from_source() == expected


def test_173():
    """Wrong argument type (int vs string)"""
    source = """
func echo(s: string) -> void {
    print(s);
}
func main() -> void {
    let a = echo(10);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(echo), [IntegerLiteral(10)])"
    assert Checker(source).check_from_source() == expected


def test_174():
    """Wrong argument type (float vs bool)"""
    source = """
func check(flag: bool) -> void {
    if (flag) { print("yes"); }
}
func main() -> void {
    let a = check(3.14);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(check), [FloatLiteral(3.14)])"
    assert Checker(source).check_from_source() == expected


def test_175():
    """Wrong argument type (array vs int)"""
    source = """
func process(x: int) -> void {}
func main() -> void {
    let a = process([1, 2, 3]);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(process), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])])"
    assert Checker(source).check_from_source() == expected


def test_176():
    """Missing all arguments"""
    source = """
func run(x: int, y: bool) -> void {}

func main() -> void {
    let a = run();
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(run), [])"
    assert Checker(source).check_from_source() == expected


def test_177():
    """Too many arguments to global function"""
    source = """
func doThing() -> void {}

func main() -> void {
    let a = doThing(1);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(doThing), [IntegerLiteral(1)])"
    assert Checker(source).check_from_source() == expected


def test_178():
    """Wrong argument type for function"""
    source = """
func greet(s: string) -> void {}

func main() -> void {
    let a = greet(true);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(greet), [BooleanLiteral(True)])"
    assert Checker(source).check_from_source() == expected


def test_179():
    """Correct number but incompatible types"""
    source = """
func compute(x: int, y: float) -> int {
    return x;
}
func main() -> void {
    let a = compute(true, "string");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(compute), [BooleanLiteral(True), StringLiteral('string')])"
    assert Checker(source).check_from_source() == expected


def test_180():
    """Mix of too few and wrong type"""
    source = """
func compare(a: int, b: int) -> bool {
    return a == b;
}
func main() -> void {
    let a = compare("one");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(compare), [StringLiteral('one')])"
    assert Checker(source).check_from_source() == expected

def test_181():
    """Assign array of different size"""
    source = '''
func main() -> void {
    let a: [int; 3] = [1, 2, 3];
    let b: [int; 5] = [1, 2, 3, 4, 5];
    a = b;
}
'''
    expected = 'Type Mismatch In Statement: Assignment(IdLValue(a), Identifier(b))'
    assert Checker(source).check_from_source() == expected


def test_182():
    """Assign float array to int array"""
    source = '''
func main() -> void {
    let a: [int; 3] = [1, 2, 3];
    let b: [float; 3] = [1.0, 2.0, 3.0];
    a = b;
}
'''
    expected = 'Type Mismatch In Statement: Assignment(IdLValue(a), Identifier(b))'
    assert Checker(source).check_from_source() == expected


def test_183():
    """Literal with incorrect type in array"""
    source = '''
func main() -> void {
    let arr: [int; 3] = [1, 2.5, 3];
}
'''
    expected = "Type Mismatch In Statement: ArrayLiteral([IntegerLiteral(1), FloatLiteral(2.5), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected


def test_184():
    """Array indexing with non-integer"""
    source = '''
func main() -> void {
    let a: [int; 3] = [1, 2, 3];
    let x = a["0"];
}
'''
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), StringLiteral('0'))"
    assert Checker(source).check_from_source() == expected


def test_185():
    """Assign multi-dimensional array with incompatible size"""
    source = '''
func main() -> void {
    let m1: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
    let m2: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
    m1 = m2;
}
'''
    expected = "Type Mismatch In Statement: Assignment(IdLValue(m1), Identifier(m2))"
    assert Checker(source).check_from_source() == expected


def test_186():
    """Assign multi-dimensional array with wrong element type"""
    source = '''
func main() -> void {
    let m1: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
    let m2: [[float; 2]; 3] = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]];
    m1 = m2;
}
'''
    expected = "Type Mismatch In Statement: Assignment(IdLValue(m1), Identifier(m2))"
    assert Checker(source).check_from_source() == expected


def test_187():
    """Assign float to element in int array"""
    source = '''
func main() -> void {
    let a: [int; 3] = [1, 2, 3];
    a[1] = 3.14;
}
'''
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected


def test_188():
    """Function call with wrong array size argument"""
    source = '''
func f(x: [int; 5]) -> void {}

func main() -> void {
    let a: [int; 3] = [1, 2, 3];
    f(a);
}
'''
    expected = "Type Mismatch In Statement: FunctionCall(Identifier(f), [Identifier(a)])"
    assert Checker(source).check_from_source() == expected


def test_189():
    """Array literal with mixed types"""
    source = '''
func main() -> void {
    let arr: [int; 3] = [1, true, 3];
}
'''
    expected = "Type Mismatch In Statement: ArrayLiteral([IntegerLiteral(1), BooleanLiteral(True), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected


def test_190():
    """Nested array element assignment with wrong type"""
    source = '''
func main() -> void {
    let m: [[int; 2]; 2] = [[1, 2], [3, 4]];
    m[0][1] = "text";
}
'''
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(ArrayAccessLValue(Identifier(m), IntegerLiteral(0)), IntegerLiteral(1)), StringLiteral('text'))"
    assert Checker(source).check_from_source() == expected