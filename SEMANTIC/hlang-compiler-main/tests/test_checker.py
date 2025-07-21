from utils import Checker


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
const PI: float = 3.14;
func main() -> void {
    let x: int = 5;
    let y = x + 1;
};
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test redeclared variable error"""
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
};
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test undeclared identifier error"""
    source = """
func main() -> void {
    let x = y + 1;
};
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test type mismatch error"""
    source = """
func main() -> void {
    let x: int = "hello";
};
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Test no main function error"""
    source = """
func hello() -> void {
    let x: int = 5;
};
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test break not in loop error"""
    source = """
func main() -> void {
    break;
};
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected
def test_007():
    """Test continue not in loop error"""
    source = """
func main() -> void {
    continue;
};
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected
def test_009():
    """Test return type mismatch in function"""
    source = """
func compute() -> int {
    return "wrong";
};

func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('wrong'))"
    assert Checker(source).check_from_source() == expected
def test_011():
    """Test array access with non-integer index"""
    source = """
func main() -> void {
    let a: [int; 5] = [1, 2, 3, 4, 5];
    let x = a["index"];
};
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), StringLiteral('index'))"
    assert Checker(source).check_from_source() == expected