from utils import Parser

def test_001():
    """Test basic function declaration"""
    source = """func main(a: int, b: int) -> int { return a + b; };"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Test function with parameters"""
    source = """func add(a: int, b: int) -> int { return a + b; };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    source = """func add() -> int { return a + b;};"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_004():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice";};"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test constant declaration"""
    source = """const PI: float = 3.14159; func main() -> void {};"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """func main() -> void { 
        if (x > 0) { 
            print("positive"); 
        } else { 
            print("negative"); 
        }
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test while loop"""
    source = """func main() -> void { 
        let i = 0;
        while (i < 10) { 
            i = i + 1; 
        }
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with array"""
    source = """func main() -> void { 
        let numbers = [1, 2, 3, 4, 5];
        for (num in numbers) { 
            print(str(num)); 
        }
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """func main() -> void { 
        let arr: [int; 3] = [1, 2, 3];
        let first = arr[0];
        arr[1] = 42;
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test complex expression with pipeline operator"""
    source = """func main() -> void { 
        let result = data >> process >> validate >> transform;
        let calculation = 5 >> add(3) >> multiply(2);
    };"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_011():
    """Test complex expression with pipeline operator"""
    source = """// This is a complete line comment
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
    expected = "success"
    assert Parser(source).parse() == expected
def test_012():
    """Test complex expression with pipeline operator"""
    source = """let numbers: [int; 5] = [1, 2, 3, 4, 5];        // Explicit size and type
let names = ["Alice", "Bob", "Charlie"];         // Size inferred as 3
let empty: [int; 0] = [];                        // Empty array with explicit type

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_013():
    """Test complex expression with pipeline operator"""
    source = """func add(a: int, b: int) -> int { return a + b; }
// Function type: (int, int) -> int

func greet(name: string) -> void { print("Hi " + name); }
// Function type: (string) -> void

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_014():
    """Test complex expression with pipeline operator"""
    source = """let x = 42;                    // Inferred as int
let y = 3.14;                  // Inferred as float
let z = true;                  // Inferred as bool
let s = "hello";               // Inferred as string (literal tokenizes as: hello)
let arr = [1, 2, 3];           // Inferred as [int; 3]

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_015():
    """Test complex expression with pipeline operator"""
    source = """let age: int = 25;                    // Explicit type annotation
let name = "Alice";                   // Type inferred as string
let pi = 3.14159;                     // Type inferred as float
let isValid = true;                   // Type inferred as bool
let numbers = [1, 2, 3, 4, 5];        // Type inferred as [int; 5]

// Reassignment (variables are mutable)
x = 15;                               // OK, x is mutable
y = y + 5;                            // OK, arithmetic reassignment

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_016():
    """Test complex expression with pipeline operator"""
    source = """const MAX_SIZE: int = 100;            // Explicit type annotation

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_017():
    """Test complex expression with pipeline operator"""
    source = """let a = 10 + 5;         // 15 (int + int = int)
let b = 3.5 + 2;        // 5.5 (float + int = float)  
let c = 10 / 3;         // 3 (integer division)
let d = 10.0 / 3;       // 3.333... (float division)
let e = 15 % 4;         // 3 (modulo)
let f = -x;             // Negation
let g = "Count: " + 42; // "Count: 42" (string concatenation)


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_018():
    """Test complex expression with pipeline operator"""
    source = """let eq1 = (5 == 5);           // true
let eq2 = (3.14 == 3.14);     // true  
let ne1 = (10 != 5);          // true
let lt1 = (3 < 5);            // true
let lt2 = (2.5 < 3);          // true (float < int)
let str1 = ("abc" < "def");   // true (lexicographic)
let str2 = ("hello" == "hello"); // true

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_019():
    """Test complex expression with pipeline operator"""
    source = """let not1 = !true;                    // false
let not2 = !false;                   // true
let and1 = true && false;            // false
let and2 = (x > 0) && (y < 10);     // Conditional AND
let or1 = true || false;             // true
let or2 = (x == 0) || (y == 0);     // Conditional OR

// Short-circuit examples:
let safe = (arr != null) && (arr[0] > 5);  // Won't access arr[0] if arr is null
let found = (result != null) || search();  // Won't call search() if result exists

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_020():
    """Test complex expression with pipeline operator"""
    source = """let numbers: [int; 5] = [10, 20, 30, 40, 50];
let first = numbers[0];        // 10 (read access)
let last = numbers[4];         // 50 (read access)
numbers[2] = 35;              // Modify element (write access)

// Dynamic indexing:
let index = 1;
let value = numbers[index];    // 20

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_021():
    """Test complex expression with pipeline operator"""
    source = """// 2D array (matrix): 2 rows, 3 columns each
let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];

// 3D array: 2 layers, 3 rows, 4 columns each  
let cube: [[[int; 4]; 3]; 2] = [
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
    [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]
];

// Jagged arrays (arrays of different-sized arrays)
let jagged: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_022():
    """Test complex expression with pipeline operator"""
    source = """// 2D array access:
let element = matrix[1][2];    // 6 (row 1, column 2)
matrix[0][1] = 99;            // Modify element in row 0, column 1

// 3D array access:
let value = cube[1][2][3];     // 24 (layer 1, row 2, column 3)
cube[0][1][2] = 100;          // Modify element

// Sequential access (equivalent to above):
let row = matrix[1];           // Get entire row: [4, 5, 6]
let element2 = row[2];         // 6 (same as matrix[1][2])

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_023():
    """Test complex expression with pipeline operator"""
    source = """// Type breakdown for [[int; 3]; 2]:
// - Outer array: [T; 2] where T = [int; 3]  
// - Inner arrays: [int; 3]
// - Elements: int

let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
// matrix has type [[int; 3]; 2]
// matrix[0] has type [int; 3] 
// matrix[0][1] has type int

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_024():
    """Test complex expression with pipeline operator"""
    source = """// Simple function calls:
let sum = add(5, 3);                    // Call with literal arguments
let result = multiply(x, y);            // Call with variable arguments  
print("Hello, World!");                 // Void function call

// Nested function calls:
let nested = add(multiply(2, 3), 4);    // 10 (6 + 4)
let chain = sqrt(abs(-16));             // Function composition

// Function expressions as arguments:
let mapped = map(numbers, square);       // Higher-order function

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_025():
    """Test complex expression with pipeline operator"""
    source = """let expr1 = 2 + 3 * 4;              // 14 (not 20) - multiplication first
let expr2 = (2 + 3) * 4;            // 20 - parentheses override precedence
let expr3 = x < 5 && y > 10;        // (x < 5) && (y > 10) - comparison first
let expr4 = !flag && condition;     // (!flag) && condition - unary first
let expr5 = a + b < c + d;          // (a + b) < (c + d) - addition before comparison
let expr6 = 5 + 3 >> multiply(2);   // (5 + 3) >> multiply(2) = 16 - pipeline lowest
let expr7 = data >> filter(isValid) >> map(transform); // Left-associative chaining

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_026():
    """Test complex expression with pipeline operator"""
    source = """// Traditional nested calls (hard to read):
let result1 = addExclamation(uppercase(trim(" hello world ")));

// Pipeline equivalent (readable left-to-right):
let result2 = " hello world " >> trim >> uppercase >> addExclamation;

// Multi-parameter function in pipeline:
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers >> map(multiply_by_two) >> filter(is_even);

// Mathematical operations in pipeline:
let calculation = 5 >> add(3) >> multiply(2) >> subtract(4);  // ((5 + 3) * 2) - 4 = 12

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_027():
    """Test complex expression with pipeline operator"""
    source = """
// Function with multiple parameters:
func formatMessage(text: string, prefix: string, suffix: string) -> string {
    return prefix + text + suffix;
}

// Pipeline passes first argument, others provided normally:
let formatted = "Hello" >> formatMessage("[", "]");  // "[Hello]"

// Equivalent to:
let formatted2 = formatMessage("Hello", "[", "]");

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_028():
    """Test complex expression with pipeline operator"""
    source = """func processInt(x: int) -> string { return "Number: " + str(x); }
func processString(s: string) -> string { return s + "!"; }

// Valid pipeline (types match):
let result = 42 >> processInt >> processString;  // "Number: 42!"

// Invalid pipeline (type mismatch):
// let invalid = "hello" >> processInt;  // Error: string cannot be passed to processInt

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_029():
    """Test complex expression with pipeline operator"""
    source = """// Pipeline has lower precedence than arithmetic:
let result = 5 + 3 >> multiply(2);     // (5 + 3) >> multiply(2) = 16

// Parentheses override precedence:
let result2 = 5 + (3 >> multiply(2));  // 5 + (3 * 2) = 11

// Multiple pipelines (left-associative):
let chain = data >> filter(isValid) >> map(transform) >> reduce(combine);
// Equivalent to: ((data >> filter(isValid)) >> map(transform)) >> reduce(combine)

// Mixed operators:
let complex = (x > 0) && (data >> process >> validate);
// Comparison and logical operations before pipeline

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_030():
    """Test complex expression with pipeline operator"""
    source = """// Efficient pipeline (fused operations):
let optimized = data >> map(transform) >> filter(isValid) >> take(10);
// Compiler may fuse these operations into a single pass

// Memory-efficient processing:
let stream = largeDataset >> 
    filter(criteria) >> 
    map(expensive_transform) >> 
    take(5);  // Only processes first 5 valid items

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_031():
    """Test complex expression with pipeline operator"""
    source = """// Type inference through pipeline:
let result = "123" >> int >> add(5) >> str;
// Types: string -> int -> int -> string

// Generic pipeline functions:
func pipeline<T, U, V>(input: T, f1: T -> U, f2: U -> V) -> V {
    return input >> f1 >> f2;
}

// Array pipeline with type preservation:
let numbers = [1, 2, 3, 4, 5];
let processed: [string; 5] = numbers >> map(str) >> sort;

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_032():
    """Test complex expression with pipeline operator"""
    source = """// Pipeline-aware function definitions:
func pipelineProcessor(input: string) -> string {
    // This function is designed for pipeline use
    return input >> validate >> clean >> format;
}

// Higher-order pipeline functions:
func createPipeline(processor: string -> string) -> (string -> string) {
    return func(input: string) -> string {
        return input >> processor >> finalize;
    };
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_033():
    """Test complex expression with pipeline operator"""
    source = """x = 10;                    // Assignment expression as statement
print("Hello World");      // Function call for side effect
factorial(5);              // Function call (result discarded)
arr[0] = 42;              // Array element assignment
++counter;                 // Increment operation (if supported)


"""
    expected = "success"
    assert Parser(source).parse() == expected
