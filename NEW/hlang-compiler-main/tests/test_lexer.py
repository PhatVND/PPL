from utils import Tokenizer
import pytest

def test_022():
    """Test basic identifier tokenization"""
    source = "\"Quote: \\\"text\\\"\""
    expected = "Quote: \\\"text\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

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
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_007():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x"
    # assert Tokenizer(source).get_tokens_as_string() == expected
    assert Tokenizer(source).get_tokens_as_string() == expected


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
def test_021():
    """Test operators and separators"""
    source = """
/* outer /* inner */ still outer */
"""
    expected = 'EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected  

def test_101():
    """Test case 101 - format changed"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_102():
    """Test case 102 - format changed"""
    source = "if"
    expected = "if,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_103():
    """Test case 103 - format changed"""
    source = "+"
    expected = "+,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_104():
    """Test case 104 - format changed"""
    source = "[]"
    expected = "[,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_105():
    """Test case 105 - format changed"""
    source = "_myVar"
    expected = "_myVar,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_106():
    """Test case 106 - format changed"""
    source = "12"
    expected = "12,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_107():
    """Test case 107 - format changed"""
    source = "0x1A"
    expected = "0,x1A,EOF" # Corrected: '0x1A' is not a single integer literal in HLang spec. '0' is int, 'x1A' is ID.
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_108():
    """Test case 108 - format changed"""
    source = "3.14"
    expected = "3.14,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_109():
    """Test case 109 - format changed"""
    source = "\"hello\""
    expected = "hello,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_110():
    """Test case 110 - format changed"""
    source = "// comment"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_111():
    """Test case 111 - format changed"""
    source = "/* block comment */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_112():
    """Test case 112 - format changed"""
    source = "^"
    expected = "Error Token ^"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_113():
    """Test case 113 - format changed"""
    source = "\"unterminated"
    expected = "Unclosed String: unterminated"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_114():
    """Test case 114 - format changed"""
    source = "\"illegal\\g\""
    expected = "Illegal Escape In String: illegal\\g"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_115():
    """Test case 115 - format changed"""
    source = "var"
    expected = "var,EOF" # 'var' is an ID in HLang spec, not a keyword. Original expected is correct based on updated spec.
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_116():
    """Test case 116 - format changed"""
    source = "type"
    expected = "type,EOF" # 'type' is an ID in HLang spec, not a keyword. Original expected is correct based on updated spec.
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_117():
    """Test case 117 - format changed"""
    source = "func"
    expected = "func,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_118():
    """Test case 118 - format changed"""
    source = "return"
    expected = "return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_119():
    """Test case 119 - format changed"""
    source = "break"
    expected = "break,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_120():
    """Test case 120 - format changed"""
    source = "continue"
    expected = "continue,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_121():
    """Test case 121 - format changed"""
    source = "nil"
    expected = "nil,EOF" # 'nil' là ID trong HLang, không phải từ khóa/literal
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_122():
    """Test case 122 - format changed"""
    source = "true"
    expected = "true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_123():
    """Test case 123 - format changed"""
    source = "false"
    expected = "false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_124():
    """Test case 124 - format changed"""
    source = "( )"
    expected = "(,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_125():
    """Test case 125 - format changed"""
    source = "{ }"
    expected = "{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_126():
    """Test case 126 - format changed"""
    source = ":="
    expected = ":,=,EOF" # Corrected: ':= 'không phải là toán tử riêng, mà là ':' và '='
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_127():
    """Test case 127 - format changed"""
    source = "=="
    expected = "==,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_128():
    """Test case 128 - format changed"""
    source = "!="
    expected = "!=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_129():
    """Test case 129 - format changed"""
    source = "<="
    expected = "<=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_130():
    """Test case 130 - format changed"""
    source = ">="
    expected = ">=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_131():
    """Test case 131 - format changed"""
    source = "5+3"
    expected = "5,+,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_132():
    """Test case 132 - format changed"""
    source = "x = 10"
    expected = "x,=,10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_133():
    """Test case 133 - format changed"""
    source = "for i := 0; i < 10; i++"
    expected = "for,i,:,=,0,;,i,<,10,;,i,++,EOF" # Corrected: ':= 'và '++' được phân tách
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_134():
    """Test case 134 - format changed"""
    source = "foo.bar"
    expected = "foo,.,bar,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_135():
    """Test case 135 - format changed"""
    source = "arr[0]"
    expected = "arr,[,0,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_136():
    """Test case 136 - format changed"""
    source = "12.e-5"
    expected = "12.e-5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_137():
    """Test case 137 - format changed"""
    source = "'c'"
    expected = "Error Token '"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_138():
    """Test case 138 - format changed"""
    source = "void"
    expected = "void,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_139():
    """Test case 139 - format changed"""
    source = "package main"
    expected = "package,main,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_140():
    """Test case 140 - format changed"""
    source = "switch"
    expected = "switch,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_141():
    """Test case 141 - format changed"""
    source = "case"
    expected = "case,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_142():
    """Test case 142 - format changed"""
    source = "default"
    expected = "default,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_143():
    """Test case 143 - format changed"""
    source = "map[string]int"
    expected = "map,[,string,],int,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_144():
    """Test case 144 - format changed"""
    source = "defer"
    expected = "defer,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_145():
    """Test case 145 - format changed"""
    source = "go"
    expected = "go,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_146():
    """Test case 146 - format changed"""
    source = "interface"
    expected = "interface,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_147():
    """Test case 147 - format changed"""
    source = "struct"
    expected = "struct,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_148():
    """Test case 148 - format changed"""
    source = "chan"
    expected = "chan,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_149():
    """Test case 149 - format changed"""
    source = "range"
    expected = "range,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_150():
    """Test case 150 - format changed"""
    source = "select"
    expected = "select,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_151():
    """Test case 151 - format changed"""
    source = """
func main() {
    var a int = 5
    var b float = 3.14
    if (a > b) {
        return "Greater"
    } else {
        return "Smaller"
    };
}
"""
    expected = "func,main,(,),{,var,a,int,=,5,var,b,float,=,3.14,if,(,a,>,b,),{,return,Greater,},else,{,return,Smaller,},;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_152():
    """Test case 152 - format changed"""
    source = """
var x int = 10;
const PI float = 3.1415;
var name string = "John Doe";
var isActive bool = true;
"""
    expected = "var,x,int,=,10,;,const,PI,float,=,3.1415,;,var,name,string,=,John Doe,;,var,isActive,bool,=,true,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_153():
    """Test case 153 - format changed"""
    source = """
if (x > 5) {
    y = x * 2;
} else if (x == 5) {
    y = x + 10;
} else {
    y = 0;
}
"""
    expected = "if,(,x,>,5,),{,y,=,x,*,2,;,},else,if,(,x,==,5,),{,y,=,x,+,10,;,},else,{,y,=,0,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_154():
    """Test case 154 - format changed"""
    source = """
for (i = 0; i < 10; i = i + 1) {
    print(i);
}
"""
    expected = "for,(,i,=,0,;,i,<,10,;,i,=,i,+,1,),{,print,(,i,),;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_155():
    """Test case 155 - format changed"""
    source = """
func factorial(n int) int {
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}
"""
    expected = "func,factorial,(,n,int,),int,{,if,(,n,==,0,),{,return,1,;,},return,n,*,factorial,(,n,-,1,),;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_156():
    """Test case 156 - format changed"""
    source = """
type Person struct {
    name string;
    age int;
    func (p Person) GetAge() int {
        return p.age;
    }
}
"""
    expected = "type,Person,struct,{,name,string,;,age,int,;,func,(,p,Person,),GetAge,(,),int,{,return,p,.,age,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_157():
    """Test case 157 - format changed"""
    source = """
var arr [5]int = [1, 2, 3, 4, 5];
"""
    expected = "var,arr,[,5,],int,=,[,1,,,2,,,3,,,4,,,5,],;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_158():
    """Test case 158 - format changed"""
    source = """
var arr = [1, 2, 3, 4, 5];
"""
    expected = "var,arr,=,[,1,,,2,,,3,,,4,,,5,],;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_159():
    """Test case 159 - format changed"""
    source = """
var arr [5]int;
"""
    expected = "var,arr,[,5,],int,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_160():
    """Test case 160 - format changed"""
    source = """
var arr;
"""
    expected = "var,arr,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_161():
    """Test case 161 - format changed"""
    source = """
break;
"""
    expected = "break,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_162():
    """Test case 162 - format changed"""
    source = """
continue;
"""
    expected = "continue,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_163():
    """Test case 163 - format changed"""
    source = """
x == 10;
"""
    expected = "x,==,10,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_164():
    """Test case 164 - format changed"""
    source = """
var name string "Hello";
"""
    expected = "var,name,string,Hello,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_165():
    """Test case 165 - format changed"""
    source = """
var str = "This is an unclosed string
"""
    expected = "var,str,=,Unclosed String: This is an unclosed string"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_166():
    """Test case 166 - format changed"""
    source = """
var str = "Hello\qWorld";
"""
    expected = "var,str,=,Illegal Escape In String: Hello\q"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_168():
    """Test case 168 - format changed"""
    source = """

type Outer struct {
    type Inner struct {
        value int;
        func (i Inner) GetValue() int {
            return i.value;
        }
    }
    /**/
    inner Inner;
    func (o Outer) GetInnerValue() int {
        return o.inner.GetValue();
    }
    // hello
}

"""
    expected = "type,Outer,struct,{,type,Inner,struct,{,value,int,;,func,(,i,Inner,),GetValue,(,),int,{,return,i,.,value,;,},},inner,Inner,;,func,(,o,Outer,),GetInnerValue,(,),int,{,return,o,.,inner,.,GetValue,(,),;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_169():
    """Test case 169 - format changed"""
    source = """
func ComplexFunction(a int, b float, c string, d [5]int, e [4]float) [3][23]int {
    var result int;
    return result
};
"""
    expected = "func,ComplexFunction,(,a,int,,,b,float,,,c,string,,,d,[,5,],int,,,e,[,4,],float,),[,3,],[,23,],int,{,var,result,int,;,return,result,},;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_170():
    """Test case 170 - format changed"""
    source = """
type ErrorStruct struct {
    name string
    age int;
    func (e ErrorStruct) GetName() string 
        return e.name;
    };
}
"""
    expected = "type,ErrorStruct,struct,{,name,string,age,int,;,func,(,e,ErrorStruct,),GetName,(,),string,return,e,.,name,;,},;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_171():
    """Test case 171 - format changed"""
    source = """
type ErrorStruct struct {
    name string
    age int;
    func (e ErrorStruct) GetName() string 
        return e.name;
    };
}"""
    expected = "type,ErrorStruct,struct,{,name,string,age,int,;,func,(,e,ErrorStruct,),GetName,(,),string,return,e,.,name,;,},;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_172():
    """Test case 172 - format changed"""
    source = """
type ErrorStruct struct {
    name string
    age int;
    /*func (e ErrorStruct) GetName() string 
        return e.name;
    };
    */
}
"""
    expected = "type,ErrorStruct,struct,{,name,string,age,int,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_173():
    """Test case 173 - format changed"""
    source = """
func Fibonacci(n int) int {
    if (n <= 1) {
        return n;
    }
    var a int = Fibonacci(n - 1) + Fibonacci(n - 2);
    return a;
}
"""
    expected = "func,Fibonacci,(,n,int,),int,{,if,(,n,<=,1,),{,return,n,;,},var,a,int,=,Fibonacci,(,n,-,1,),+,Fibonacci,(,n,-,2,),;,return,a,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_174():
    """Test case 174 - format changed"""
    source = """
for (i = 0; i < 100; i = i + 1) {
    if (i % 2 == 0) {
        continue;
    } else if (i == 55) {
        break;
    }
    print(i);
}
"""
    expected = "for,(,i,=,0,;,i,<,100,;,i,=,i,+,1,),{,if,(,i,%,2,==,0,),{,continue,;,},else,if,(,i,==,55,),{,break,;,},print,(,i,),;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_175():
    """Test case 175 - format changed"""
    source = """
var unknownType myCustomType = 10;
"""
    expected = "var,unknownType,myCustomType,=,10,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_176():
    """Test case 176 - format changed"""
    source = """
var _variable$Name123 string = "Hello, World!";
"""
    expected = "var,_variable,Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_177():
    """Test case 177 - format changed"""
    source = """
var result float = 10 / 0;
"""
    expected = "var,result,float,=,10,/,0,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_178():
    """Test case 178 - format changed"""
    source = """
var a int = "string_value";
"""
    expected = "var,a,int,=,string_value,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_179():
    """Test case 179 - format changed"""
    source = """
func NoReturn() int {
    return;
}
"""
    expected = "func,NoReturn,(,),int,{,return,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_180():
    """Test case 180 - format changed"""
    source = """
func NoReturn() int {
    
}
"""
    expected = "func,NoReturn,(,),int,{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_181():
    """Test case 181 - format changed"""
    source = """
func NoReturn(a, b, c, d, e int, asd float, trh6h string) int {return;}
"""
    expected = "func,NoReturn,(,a,,,b,,,c,,,d,,,e,int,,,asd,float,,,trh6h,string,),int,{,return,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_182():
    """Test case 182 - format changed"""
    source = """
func NestedIf(x int) string {
    if (x > 0) {
        if (x > 10) {
            return "Greater than 10"
        } else {
            if (x == 5) {
                return "Equal to 5"
            } else {
                return "Between 1 and 10"
            }
        }
    } else {
        return "Negative"
    }
}
"""
    expected = "func,NestedIf,(,x,int,),string,{,if,(,x,>,0,),{,if,(,x,>,10,),{,return,Greater than 10,},else,{,if,(,x,==,5,),{,return,Equal to 5,},else,{,return,Between 1 and 10,},},},else,{,return,Negative,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_183():
    """Test case 183 - format changed"""
    source = """
func MissingBrace() int 
    return 10;
"""
    expected = "func,MissingBrace,(,),int,return,10,;,EOF" # Corrected: Removed extra ';' after 'int'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_184():
    """Test case 184 - format changed"""
    source = """
func NoReturnValue() string {
}
"""
    expected = "func,NoReturnValue,(,),string,{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_185():
    """Test case 185 - format changed"""
    source = """
func UndefinedVariable() {
    x = 10;
}
"""
    expected = "func,UndefinedVariable,(,),{,x,=,10,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_186():
    """Test case 186 - format changed"""
    source = """
type InvalidStruct struct {
    name string;
    age unknownType;
}
"""
    expected = "type,InvalidStruct,struct,{,name,string,;,age,unknownType,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_187():
    """Test case 187 - format changed"""
    source = """
var str string = "Hello \q World!";
"""
    expected = "var,str,string,=,Illegal Escape In String: Hello \q"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_189():
    """Test case 189 - format changed"""
    source = """
func InvalidParams(x int, y string z float) {
    return;
}
"""
    expected = "func,InvalidParams,(,x,int,,,y,string,z,float,),{,return,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_190():
    """Test case 190 - format changed"""
    source = """
type DuplicateField struct {
    name string;
    name int;
}
"""
    expected = "type,DuplicateField,struct,{,name,string,;,name,int,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_191():
    """Test case 191 - format changed"""
    source = """
var result = 10 === 10;
"""
    expected = "var,result,=,10,==,=,10,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_192():
    """Test case 192 - format changed"""
    source = """
var specialVar = @#$%^&*();
"""
    expected = "var,specialVar,=,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_193():
    """Test case 193 - format changed"""
    source = """
func Outer() {
    func Inner() {
        print("Inner function");
    }
    Inner();
}
"""
    expected = "func,Outer,(,),{,func,Inner,(,),{,print,(,Inner function,),;,},Inner,(,),;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_194():
    """Test case 194 - format changed"""
    source = """
var arr [5]int = [1, 2, 3, 4, 5];
"""
    expected = "var,arr,[,5,],int,=,[,1,,,2,,,3,,,4,,,5,],;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_195():
    """Test case 195 - format changed"""
    source = """
`
"""
    expected = "Error Token `"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_196():
    """Test case 196 - format changed"""
    source = """
nil
"""
    expected = "nil,EOF" # Corrected: Removed extra ';'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_197():
    """Test case 197 - format changed"""
    source = """
/* test
*/ a /* */
"""
    expected = "a,EOF" # Corrected: Removed extra ';'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_198():
    """Test case 198 - format changed"""
    source = """
type Person struct {
    func (p Person) Greet() string {
        return "Hello, " + p.name
    }; c c;
    func (p Person) Greet() string {
        return "Hello, " + p.name
    } c c;
}
"""
    expected = "type,Person,struct,{,func,(,p,Person,),Greet,(,),string,{,return,Hello, ,+,p,.,name,},;,c,c,;,func,(,p,Person,),Greet,(,),string,{,return,Hello, ,+,p,.,name,},c,c,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_199():
    """Test case 199 - format changed"""
    source = """
func (p Person) Greet() string {
    if (1) {return;}
    else if (1)
    {}
};
"""
    expected = "func,(,p,Person,),Greet,(,),string,{,if,(,1,),{,return,;,},else,if,(,1,),{,},},;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_200():
    """Test case 200 - format changed"""
    source = """
type Person struct {
    /* func (p Person) Greet() string {
        return "Hello, " + p.name
    }
    */
    c c
    func (c c) Add(x, y int, b float) {return ;}
    value int;
}
"""
    expected = "type,Person,struct,{,c,c,func,(,c,c,),Add,(,x,,,y,int,,,b,float,),{,return,;,},value,int,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected