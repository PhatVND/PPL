from utils import ASTGenerator


def test_001():
    """Test basic constant declaration AST generation"""
    source = """    func main() -> void {
        let array = [10, 20];
        for (a in array){
            print("" + a);
        }
    }
}"""
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(42))])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


