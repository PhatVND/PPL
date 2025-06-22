from utils import Tokenizer
import pytest
from lexererr import UncloseString
from lexererr import IllegalEscape 

def test_001():
    """Test basic identifier tokenization"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test keywords recognition"""
    source = "func main if else while for let const"
    expected = "func,main,if,else,while,for,let,const,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test integer literals"""
    source = "42 0 -17 007"
    expected = "42,0,-,17,007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test float literals"""
    source = "3.14 -2.5 0.0 42. 5."
    expected = "3.14,-,2.5,0.0,42.,5.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_005():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_006():
    """Test unclosed string literal error"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    # assert Tokenizer(source).get_tokens_as_string() == expected
    with pytest.raises(UncloseString) as excinfo:
        Tokenizer(source).get_tokens_as_string()
    assert str(excinfo.value) == expected


def test_007():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x World"
    # assert Tokenizer(source).get_tokens_as_string() == expected
    with pytest.raises(IllegalEscape) as excinfo:
        Tokenizer(source).get_tokens_as_string()
    assert str(excinfo.value) == expected


def test_008():
    """Test error character (non-ASCII or invalid character)"""
    source = "let x = 5; @ invalid"
    expected = "let,x,=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009():
    """Test valid string literals with escape sequences"""
    source = '"Hello World" "Line 1\\nLine 2" "Quote: \\"text\\""'
    expected = 'Hello World,Line 1\\nLine 2,Quote: \\"text\\",EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_010():
    """Test operators and separators"""
    source = "+ - * / % == != < <= > >= && || ! = -> >> ( ) [ ] { } , ; :"
    expected = "+,-,*,/,%,==,!=,<,<=,>,>=,&&,||,!,=,->,>>,(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_011():
    """Test operators and separators"""
    source = 'let msg = "Café";      // Compile error: non-ASCII in string'
    expected = "let,msg,=,Error Token \""
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_012():
    """Test operators and separators"""
    source = "/* THIS IS COMMENT */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_013():
    """Test operators and separators"""
    source = 'let greeting = "Hello, World!";'
    expected = 'let,greeting,=,Hello, World!,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_014():
    """Test operators and separators"""
    source = """
// This is a complete line comment
let x = 42;        // End-of-line comment explaining variable

// Multiple single-line comments
// can be used to create
// multi-line documentation

func factorial(n: int) -> int {
    // Base case: factorial of 0 or 1 is 1
    if (n <= 1) {
        return 1;   // Return base case value
    }
    // Recursive case: n! = n * (n-1)!
    return n * factorial(n - 1);
}

// Commenting out code for debugging
// let debugValue = computeExpensiveOperation();
let result = simpleOperation();
"""
    expected = 'let,x,=,42,;,func,factorial,(,n,:,int,),->,int,{,if,(,n,<=,1,),{,return,1,;,},return,n,*,factorial,(,n,-,1,),;,},let,result,=,simpleOperation,(,),;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_015():
    """Test operators and separators"""
    source = """
/*
 * Multi-line block comment
 * describing the following function
 * Author: John Doe
 * Date: June 2025
 */
func complexCalculation(data: [int; 10]) -> float {
    /* This algorithm implements the
       advanced mathematical formula
       discovered by Smith et al. */
    
    let result = 0.0;
    /* Loop through all elements */ for (item in data) {
        result = result + float(item);
    }
    return result / 10.0;  /* Calculate average */
}

/* Nested comments example */
/*
 * Outer comment begins here
 * /* Inner comment can contain code:
 *    let x = 42;
 *    let y = x * 2;
 * */ 
 * Outer comment continues after inner ends
 */

/* Temporarily disable entire function
func debugFunction() -> void {
    print("Debug output");
    /* Even nested comments work here
       let temp = calculate();
    */
}
*/

"""
    expected = 'func,complexCalculation,(,data,:,[,int,;,10,],),->,float,{,let,result,=,0.0,;,for,(,item,in,data,),{,result,=,result,+,float,(,item,),;,},return,result,/,10.0,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_016():
    """Test operators and separators"""
    source = """

"""
    expected = 'EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_017():
    """Test operators and separators"""
    source = """
    let names = ["Alice", "Bob", "Charlie"]; 
"""
    expected = 'let,names,=,[,Alice,,,Bob,,,Charlie,],;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_018():
    """Test operators and separators"""
    source = """
    let f = -x; 
"""
    expected = 'let,f,=,-,x,;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_019():
    """Test operators and separators"""
    source = """
let stream = largeDataset >> 
    filter(criteria) >> 
    map(expensive_transform) >> 
    take(5);  // Only processes first 5 valid items

"""
    expected = 'let,stream,=,largeDataset,>>,filter,(,criteria,),>>,map,(,expensive_transform,),>>,take,(,5,),;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  
def test_020():
    """Test operators and separators"""
    source = """
func multiply(x: int, y: int) -> int { return x * y; }
// Type: (int, int) -> int

func greet(name: string) -> void { print("Hi " + name); }
// Type: (string) -> void

func getPI() -> float { return 3.14159; }
// Type: () -> float

"""
    expected = 'func,multiply,(,x,:,int,,,y,:,int,),->,int,{,return,x,*,y,;,},func,greet,(,name,:,string,),->,void,{,print,(,Hi ,+,name,),;,},func,getPI,(,),->,float,{,return,3.14159,;,},EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  