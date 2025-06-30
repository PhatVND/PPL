from utils import Parser

def test_001():
    """Test basic function declaration"""
    source = """func main(a: int, b: int) -> int { let x = 5; return a + b; };"""
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
const x = 42;        // End-of-line comment explaining variable

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
    expected = "Error on line 19 col 0: let"
    assert Parser(source).parse() == expected
def test_012():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
        let numbers: [int; 5] = [1, 2, 3, 4, 5];        // Explicit size and type
        let names = ["Alice", "Bob", "Charlie"];         // Size inferred as 3
        let empty: [int; 0] = [];                        // Empty array with explicit type
    };
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
    source = """
    func main() -> void {
    let x = 42;                    // Inferred as int
let y = 3.14;                  // Inferred as float
let z = true;                  // Inferred as bool
let s = "hello";               // Inferred as string (literal tokenizes as: hello)
let arr = [1, 2, 3];           // Inferred as [int; 3]
    };
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_015():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    let age: int = 25;                    // Explicit type annotation
let name = "Alice";                   // Type inferred as string
let pi = 3.14159;                     // Type inferred as float
let isValid = true;                   // Type inferred as bool
let numbers = [1, 2, 3, 4, 5];        // Type inferred as [int; 5]

// Reassignment (variables are mutable)
x = 15;                               // OK, x is mutable
y = y + 5;                            // OK, arithmetic reassignment
}
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
    source = """
    func main() -> void {
    let a = 10 + 5;         // 15 (int + int = int)
let b = 3.5 + 2;        // 5.5 (float + int = float)  
let c = 10 / 3;         // 3 (integer division)
let d = 10.0 / 3;       // 3.333... (float division)
let e = 15 % 4;         // 3 (modulo)
let f = -x;             // Negation
let g = "Count: " + 42; // "Count: 42" (string concatenation)
    }

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_018():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    let eq1 = (5 == 5);           // true
let eq2 = (3.14 == 3.14);     // true  
let ne1 = (10 != 5);          // true
let lt1 = (3 < 5);            // true
let lt2 = (2.5 < 3);          // true (float < int)
let str1 = ("abc" < "def");   // true (lexicographic)
let str2 = ("hello" == "hello"); // true
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_019():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    let not1 = !true;                    // false
let not2 = !false;                   // true
let and1 = true && false;            // false
let and2 = (x > 0) && (y < 10);     // Conditional AND
let or1 = true || false;             // true
let or2 = (x == 0) || (y == 0);     // Conditional OR

// Short-circuit examples:
let safe = (arr != null) && (arr[0] > 5);  // Won't access arr[0] if arr is null
let found = (result != null) || search();  // Won't call search() if result exists
    }
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_020():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    let numbers: [int; 5] = [10, 20, 30, 40, 50];
let first = numbers[0];        // 10 (read access)
let last = numbers[4];         // 50 (read access)
numbers[2] = 35;              // Modify element (write access)

// Dynamic indexing:
let index = 1;
let value = numbers[index];    // 20
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_021():
    """Test complex expression with pipeline operator"""
    source = """// 2D array (matrix): 2 rows, 3 columns each
    func main() -> void {
    let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];

// 3D array: 2 layers, 3 rows, 4 columns each  
let cube: [[[int; 4]; 3]; 2] = [
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
    [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]
];

// Jagged arrays (arrays of different-sized arrays)
let jagged: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_022():
    """Test complex expression with pipeline operator"""
    source = """// 2D array access:
 func main() -> void {
    let element = matrix[1][2];    // 6 (row 1, column 2)
matrix[0][1] = 99;            // Modify element in row 0, column 1

// 3D array access:
let value = cube[1][2][3];     // 24 (layer 1, row 2, column 3)
cube[0][1][2] = 100;          // Modify element

// Sequential access (equivalent to above):
let row = matrix[1];           // Get entire row: [4, 5, 6]
let element2 = row[2];         // 6 (same as matrix[1][2])
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_023():
    """Test complex expression with pipeline operator"""
    source = """// Type breakdown for [[int; 3]; 2]:
// - Outer array: [T; 2] where T = [int; 3]  
// - Inner arrays: [int; 3]
// - Elements: int
func main() -> void {
let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
// matrix has type [[int; 3]; 2]
// matrix[0] has type [int; 3] 
// matrix[0][1] has type int
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_024():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Simple function calls:
let sum = add(5, 3);                    // Call with literal arguments
let result = multiply(x, y);            // Call with variable arguments  
print("Hello, World!");                 // Void function call

// Nested function calls:
let nested = add(multiply(2, 3), 4);    // 10 (6 + 4)
let chain = sqrt(abs(-16));             // Function composition

// Function expressions as arguments:
let mapped = map(numbers, square);       // Higher-order function
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_025():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    let expr1 = 2 + 3 * 4;              // 14 (not 20) - multiplication first
let expr2 = (2 + 3) * 4;            // 20 - parentheses override precedence
let expr3 = x < 5 && y > 10;        // (x < 5) && (y > 10) - comparison first
let expr4 = !flag && condition;     // (!flag) && condition - unary first
let expr5 = a + b < c + d;          // (a + b) < (c + d) - addition before comparison
let expr6 = 5 + 3 >> multiply(2);   // (5 + 3) >> multiply(2) = 16 - pipeline lowest
let expr7 = data >> filter(isValid) >> map(transform); // Left-associative chaining
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_026():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Traditional nested calls (hard to read):
let result1 = addExclamation(uppercase(trim(" hello world ")));

// Pipeline equivalent (readable left-to-right):
let result2 = " hello world " >> trim >> uppercase >> addExclamation;

// Multi-parameter function in pipeline:
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers >> map(multiply_by_two) >> filter(is_even);

// Mathematical operations in pipeline:
let calculation = 5 >> add(3) >> multiply(2) >> subtract(4);  // ((5 + 3) * 2) - 4 = 12
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_027():
    """Test complex expression with pipeline operator"""
    source = """
func main() -> void {
    // Function with multiple parameters:
func formatMessage(text: string, prefix: string, suffix: string) -> string {
    return prefix + text + suffix;
}

// Pipeline passes first argument, others provided normally:
let formatted = "Hello" >> formatMessage("[", "]");  // "[Hello]"

// Equivalent to:
let formatted2 = formatMessage("Hello", "[", "]");
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_028():
    """Test complex expression with pipeline operator"""
    source = """func processInt(x: int) -> string { return "Number: " + str(x); }
func processString(s: string) -> string { return s + "!"; }
func main() -> void {
// Valid pipeline (types match):
let result = 42 >> processInt >> processString;  // "Number: 42!"

// Invalid pipeline (type mismatch):
// let invalid = "hello" >> processInt;  // Error: string cannot be passed to processInt
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_029():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Pipeline has lower precedence than arithmetic:
let result = 5 + 3 >> multiply(2);     // (5 + 3) >> multiply(2) = 16

// Parentheses override precedence:
let result2 = 5 + (3 >> multiply(2));  // 5 + (3 * 2) = 11

// Multiple pipelines (left-associative):
let chain = data >> filter(isValid) >> map(transform) >> reduce(combine);
// Equivalent to: ((data >> filter(isValid)) >> map(transform)) >> reduce(combine)

// Mixed operators:
let complex = (x > 0) && (data >> process >> validate);
// Comparison and logical operations before pipeline
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_030():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Efficient pipeline (fused operations):
let optimized = data >> map(transform) >> filter(isValid) >> take(10);
// Compiler may fuse these operations into a single pass

// Memory-efficient processing:
let stream = largeDataset >> 
    filter(criteria) >> 
    map(expensive_transform) >> 
    take(5);  // Only processes first 5 valid items
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_031():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Type inference through pipeline:
let result = "123" >> int >> add(5) >> str;
// Types: string -> int -> int -> string

// Generic pipeline functions:
func pipeline<T, U, V>(input: T, f1: T -> U, f2: U -> V) -> V {
    return input >> f1 >> f2;
}

// Array pipeline with type preservation:
let numbers = [1, 2, 3, 4, 5];
let processed: [string; 5] = numbers >> map(str) >> sort;
}
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
    source = """
    func main() -> void {
    x = 10;                    // Assignment expression as statement
print("Hello World");      // Function call for side effect
factorial(5);              // Function call (result discarded)
arr[0] = 42;              // Array element assignment
++counter;                 // Increment operation (if supported)
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_034():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    let age: int = 25;                    // Explicit type annotation
let name = "Alice";                   // Type inferred as string
let pi = 3.14159;                     // Type inferred as float
let numbers = [1, 2, 3, 4, 5];       // Type inferred as [int; 5]
let isValid: bool = checkInput();     // Type annotation with function call

// Shadowing example:
let x = 10;                           // Outer x (int)
{
    let x = "hello";                  // Inner x (string) - shadows outer x
    // Inner x is accessible here
}
// Outer x is accessible again here
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_035():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Variable assignment:
let x: int = 10;
x = 20;                              // Simple assignment
x = x + 5;                           // Self-referential assignment

// Array element assignment:
let numbers: [int; 3] = [1, 2, 3];
numbers[0] = 10;                     // Single element
numbers[1] = numbers[2] + 5;         // Expression assignment

// Multi-dimensional assignment:
let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
matrix[0][1] = 99;                   // 2D array assignment

// Error cases:
const PI = 3.14159;
// PI = 2.71828;                     // Error: cannot assign to const
// numbers[5] = 10;                  // Runtime error: index out of bounds
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_036():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Simple if statement:
if (age >= 18) {
    print("Adult");
}

// If-else statement:
if (score >= 90) {
    grade = "A";
} else {
    grade = "B";
}

// Multiple conditions:
if (temperature > 30) {
    print("Hot weather");
} else if (temperature > 20) {
    print("Warm weather");
} else if (temperature > 10) {
    print("Cool weather");
} else {
    print("Cold weather");
}

// Nested conditionals:
if (user.isLoggedIn) {
    if (user.isAdmin) {
        showAdminPanel();
    } else {
        showUserPanel();
    }
}

// Complex conditions:
if ((age >= 18 && hasLicense) || isEmergency) {
    allowDriving = true;
}
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_037():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Basic counting loop:
let i = 0;
while (i < 10) {
    print("Count: " + str(i));
    i = i + 1;
}

// Input validation loop:
let input: string;
while (input != "quit") {
    input = getUserInput();
    processInput(input);
}

// Infinite loop (requires break to exit):
while (true) {
    let command = getCommand();
    if (command == "exit") {
        break;
    }
    executeCommand(command);
}
}


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_038():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Array iteration:
let numbers = [1, 2, 3, 4, 5];
for (num in numbers) {
    print("Number: " + str(num));
}

// String iteration (if strings are iterable):
let text = "Hello";
for (char in text) {
    print("Character: " + char);
}

// Multi-dimensional array iteration:
let matrix = [[1, 2], [3, 4], [5, 6]];
for (row in matrix) {
    for (element in row) {
        print(str(element));
    }
}

// Processing with conditions:
let scores = [85, 92, 78, 96, 88];
for (score in scores) {
    if (score >= 90) {
        print("Excellent: " + str(score));
    }
}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_039():
    """Test complex expression with pipeline operator"""
    source = """
    
    func main() -> void {
    // Early loop termination:
let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
for (num in numbers) {
    if (num > 5) {
        break;  // Exit loop when number exceeds 5
    }
    print(str(num));
}
// Prints: 1, 2, 3, 4, 5

// Search with early exit:
let found = false;
let target = 7;
for (value in data) {
    if (value == target) {
        found = true;
        break;  // Stop searching once found
    }
}
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_040():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // Skip even numbers:
for (i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) {
    if (i % 2 == 0) {
        continue;  // Skip even numbers
    }
    print("Odd: " + str(i));
}
// Prints: Odd: 1, Odd: 3, Odd: 5, Odd: 7, Odd: 9

// Data filtering:
for (item in dataList) {
    if (!isValid(item)) {
        continue;  // Skip invalid items
    }
    processItem(item);
}

}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_041():
    """Test complex expression with pipeline operator"""
    source = """// Void function return:
func printGreeting(name: string) -> void {
    if (name == "") {
        return;  // Early return for empty name
    }
    print("Hello, " + name + "!");
}

// Non-void function:
func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;  // Base case
    }
    return n * factorial(n - 1);  // Recursive case
}

// Multiple return paths:
func findMax(a: int, b: int) -> int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
    // All paths must return a value
}

// Early return pattern:
func processUser(user: User) -> bool{
    if (!user.isValid()) {
        return false;  // Early failure return
    }
    
    if (!user.hasPermission()) {
        return false;  // Another early return
    }
    
    // Main processing logic
    user.process();
    return true;  // Success return
}



"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_042():
    """Test complex expression with pipeline operator"""
    source = """// Explicit block for scoping:
    func main() -> void {
{
    let tempVar = computeValue();
    let result = processValue(tempVar);
    // tempVar and result are not accessible outside this block
}

// Nested scoping:
let x = 10;
{
    let y = 20;
    {
        let z = 30;
        // x, y, z all accessible here
        let x = 100;  // Shadows outer x
        // Here: x = 100, y = 20, z = 30
    }
    // Here: x = 10 (original), y = 20, z not accessible
}
// Here: only x = 10 accessible
}


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_043():
    """Test complex expression with pipeline operator"""
    source = """// Function with multiple parameters:
func add(a: int, b: int) -> int {
    return a + b;
}

// Function with no parameters:
func getCurrentTime() -> string {
    return getSystemTime();
}

// Void function:
func printGreeting(name: string) -> void {
    print("Hello, " + name + "!");
}

// Function with array parameter:
func sumArray(numbers: [int; 5]) -> int {
    let total = 0;
    for (num in numbers) {
        total = total + num;
    }
    return total;
}

// Function with mixed parameter types:
func formatScore(name: string, score: int, isPassing: bool) -> string {
    let status = isPassing ? "PASS" : "FAIL";
    return name + ": " + str(score) + " (" + status + ")";
}


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_044():
    """Test complex expression with pipeline operator"""
    source = """func multiply(x: int, y: int) -> int { return x * y; }
// Type: (int, int) -> int

func greet(name: string) -> void { print("Hi " + name); }
// Type: (string) -> void

func getPI() -> float { return 3.14159; }
// Type: () -> float


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_045():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    func modifyInt(x: int) -> void {
    x = 100;  // Only modifies local parameter copy
}

let value = 42;
modifyInt(value);
// value is still 42 after function call
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_046():
    """Test complex expression with pipeline operator"""
    source = """func processString(text: string) -> string {
    // Cannot modify text parameter directly
    return text + " processed";
}
func main() -> void {
let original = "data";
let result = processString(original);
// original remains "data", result is "data processed"
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_047():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    func fillArray(arr: [int; 3], value: int) -> void {
    for (i in [0, 1, 2]) {
        arr[i] = value;  // Modifies original array
    }
}

let numbers = [1, 2, 3];
fillArray(numbers, 99);
// numbers is now [99, 99, 99]
}
"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_048():
    """Test complex expression with pipeline operator"""
    source = """const globalConst = 100;  // Global scope

func example(param: int) -> int {
    // param is function-scoped
    let localVar = param * 2;  // Function-scoped local variable
    
    {
        let blockVar = localVar + 1;  // Block-scoped variable
        if (blockVar > 10) {
            let conditionVar = blockVar / 2;  // Conditional block scope
            return conditionVar;
        }
        // conditionVar not accessible here
    }
    // blockVar not accessible here
    
    return localVar + globalConst;  // Can access global const
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_049():
    """Test complex expression with pipeline operator"""
    source = """// Valid: All paths return
func absoluteValue(x: int) -> int {
    if (x >= 0) {
        return x;     // Path 1: return positive value
    } else {
        return -x;    // Path 2: return negated value
    }
    // Both paths covered
}

// Valid: Single return path
func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Error: Missing return on some paths
func badFunction(x: int) -> int {
    if (x > 0) {
        return x;
    }
    // Error: No return for x <= 0 case
}

// Valid: Void function with early return
func printPositive(x: int) -> void {
    if (x <= 0) {
        return;  // Early exit for non-positive values
    }
    print("Positive: " + str(x));
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_050():
    """Test complex expression with pipeline operator"""
    source = """func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

func fibonacci(n: int) -> int {
    if (n <= 1) {
        return n;                    // Base cases: fib(0)=0, fib(1)=1
    }
    return fibonacci(n - 1) + fibonacci(n - 2);  // Recursive calls
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_051():
    """Test complex expression with pipeline operator"""
    source = """func isEven(n: int) -> bool {
    if (n == 0) {
        return true;
    }
    return isOdd(n - 1);             // Calls isOdd
}

func isOdd(n: int) -> bool {
    if (n == 0) {
        return false;
    }
    return isEven(n - 1);            // Calls isEven
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_052():
    """Test complex expression with pipeline operator"""
    source = """
    func main() -> void {
    // String conversion examples:
let age = 25;
let ageStr = str(age);            // "25"

let pi = 3.14159;
let piStr = str(pi);              // "3.14159"

let isValid = true;
let validStr = str(isValid);      // "true"

// Parsing examples:
let numStr = "42";
let num = int(numStr);            // 42

let floatStr = "3.14";
let floatNum = float(floatStr);   // 3.14

// Error cases (runtime errors):
// let invalid = int("not_a_number");  // Runtime error
// let invalid2 = float("abc");        // Runtime error
}

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_053():
    """Test complex expression with pipeline operator"""
    source = """func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

func main() -> void {
    let num = 5;
    let result = factorial(num);
    print("Factorial of " + str(num) + " is " + str(result));
}


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_054():
    """Test complex expression with pipeline operator"""
    source = """func sum_array(arr: [int; 5]) -> int {
    let total = 0;
    for (element in arr) {
        total = total + element;
    }
    return total;
}

func main() -> void {
    let numbers: [int; 5] = [1, 2, 3, 4, 5];
    let sum = sum_array(numbers);
    print("Sum of array: " + str(sum));
}


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_055():
    """Test complex expression with pipeline operator"""
    source = """func add(a: float, b: float) -> float {
    return a + b;
}

func multiply(a: float, b: float) -> float {
    return a * b;
}

func main() -> void {
    let x = 10.5;
    let y = 3.2;
    
    print("Addition: " + str(add(x, y)));
    print("Multiplication: " + str(multiply(x, y)));
}



"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_201():
    """Kiểm tra chương trình không hợp lệ với một định danh."""
    source = """abc"""
    expected = "Error on line 1 col 0: abc"
    assert Parser(source).parse() == expected

def test_202():
    """Kiểm tra chương trình không hợp lệ với một từ khóa (if)."""
    source = """if"""
    expected = "Error on line 1 col 0: if"
    assert Parser(source).parse() == expected

def test_203():
    """Kiểm tra chương trình không hợp lệ với một toán tử (+)."""
    source = """+"""
    expected = "Error on line 1 col 0: +"
    assert Parser(source).parse() == expected

def test_204():
    """Kiểm tra chương trình không hợp lệ với dấu ngoặc vuông."""
    source = """[]"""
    expected = "Error on line 1 col 0: ["
    assert Parser(source).parse() == expected

def test_205():
    """Kiểm tra chương trình không hợp lệ với định danh bắt đầu bằng dấu gạch dưới."""
    source = """_mylet"""
    expected = "Error on line 1 col 0: _mylet"
    assert Parser(source).parse() == expected

def test_206():
    """Kiểm tra chương trình không hợp lệ với một số nguyên."""
    source = """12"""
    expected = "Error on line 1 col 0: 12"
    assert Parser(source).parse() == expected

def test_208():
    """Kiểm tra chương trình không hợp lệ với một số thực."""
    source = """3.14"""
    expected = "Error on line 1 col 0: 3.14"
    assert Parser(source).parse() == expected

def test_209():
    """Kiểm tra chương trình không hợp lệ với một chuỗi ký tự."""
    source = """\"hello\""""
    expected = "Error on line 1 col 0: hello"
    assert Parser(source).parse() == expected

def test_210():
    """Kiểm tra chương trình chỉ chứa một comment một dòng."""
    source = """// comment"""
    expected = "Error on line 1 col 10: <EOF>"
    assert Parser(source).parse() == expected

def test_211():
    """Kiểm tra chương trình chỉ chứa một comment đa dòng."""
    source = """/* block comment */"""
    expected = "Error on line 1 col 19: <EOF>"
    assert Parser(source).parse() == expected

def test_215():
    """Kiểm tra chương trình không hợp lệ với định danh (let)."""
    source = """let"""
    expected = "Error on line 1 col 0: let"
    assert Parser(source).parse() == expected

def test_216():
    """Kiểm tra chương trình không hợp lệ với định danh (type)."""
    source = """type"""
    expected = "Error on line 1 col 0: type"
    assert Parser(source).parse() == expected

def test_217():
    """Kiểm tra khai báo hàm không hoàn chỉnh."""
    source = """func"""
    expected = "Error on line 1 col 4: <EOF>"
    assert Parser(source).parse() == expected

def test_218():
    """Kiểm tra chương trình không hợp lệ với từ khóa return."""
    source = """return"""
    expected = "Error on line 1 col 0: return"
    assert Parser(source).parse() == expected

def test_219():
    """Kiểm tra chương trình không hợp lệ với từ khóa break."""
    source = """break"""
    expected = "Error on line 1 col 0: break"
    assert Parser(source).parse() == expected

def test_220():
    """Kiểm tra chương trình không hợp lệ với từ khóa continue."""
    source = """continue"""
    expected = "Error on line 1 col 0: continue"
    assert Parser(source).parse() == expected

def test_221():
    """Kiểm tra chương trình với định danh 'nil' không hợp lệ."""
    source = """nil"""
    expected = "Error on line 1 col 0: nil"
    assert Parser(source).parse() == expected

def test_222():
    """Kiểm tra chương trình với giá trị boolean 'true' không hợp lệ."""
    source = """true"""
    expected = "Error on line 1 col 0: true"
    assert Parser(source).parse() == expected

def test_223():
    """Kiểm tra chương trình với giá trị boolean 'false' không hợp lệ."""
    source = """false"""
    expected = "Error on line 1 col 0: false"
    assert Parser(source).parse() == expected

def test_224():
    """Kiểm tra chương trình chỉ với dấu ngoặc đơn rỗng không hợp lệ."""
    source = """( )"""
    expected = "Error on line 1 col 0: ("
    assert Parser(source).parse() == expected

def test_225():
    """Kiểm tra chương trình chỉ với dấu ngoặc nhọn rỗng không hợp lệ."""
    source = """{ }"""
    expected = "Error on line 1 col 0: {"
    assert Parser(source).parse() == expected

def test_226():
    """Kiểm tra chương trình với toán tử không hợp lệ ':='."""
    source = """:="""
    expected = "Error on line 1 col 0: :" # Sửa lỗi này để phản ánh lỗi lexer phân tách ':=' thành ':' và '='
    assert Parser(source).parse() == expected

def test_227():
    """Kiểm tra chương trình với toán tử '==' không hợp lệ."""
    source = """=="""
    expected = "Error on line 1 col 0: =="
    assert Parser(source).parse() == expected

def test_228():
    """Kiểm tra chương trình với toán tử '!=' không hợp lệ."""
    source = """!="""
    expected = "Error on line 1 col 0: !="
    assert Parser(source).parse() == expected

def test_229():
    """Kiểm tra chương trình với toán tử '<=' không hợp lệ."""
    source = """<="""
    expected = "Error on line 1 col 0: <="
    assert Parser(source).parse() == expected

def test_230():
    """Kiểm tra chương trình với toán tử '>=' không hợp lệ."""
    source = """>="""
    expected = "Error on line 1 col 0: >="
    assert Parser(source).parse() == expected

def test_231():
    """Kiểm tra chương trình với biểu thức số học không hợp lệ."""
    source = """5+3"""
    expected = "Error on line 1 col 0: 5"
    assert Parser(source).parse() == expected

def test_232():
    """Kiểm tra chương trình với câu lệnh gán không hợp lệ."""
    source = """x = 10"""
    expected = "Error on line 1 col 0: x"
    assert Parser(source).parse() == expected

def test_233():
    """Kiểm tra chương trình với vòng lặp 'for' không hợp lệ."""
    source = """for i := 0; i < 10; i++"""
    expected = "Error on line 1 col 0: for"
    assert Parser(source).parse() == expected

def test_234():
    """Kiểm tra chương trình với truy cập thành viên không hợp lệ."""
    source = """foo.bar"""
    expected = "Error on line 1 col 0: foo"
    assert Parser(source).parse() == expected

def test_235():
    """Kiểm tra chương trình với truy cập mảng không hợp lệ."""
    source = """arr[0]"""
    expected = "Error on line 1 col 0: arr"
    assert Parser(source).parse() == expected

def test_236():
    """Kiểm tra chương trình với số thực dạng khoa học không hợp lệ."""
    source = """12.e-5"""
    expected = "Error on line 1 col 0: 12.e-5"
    assert Parser(source).parse() == expected


def test_238():
    """Kiểm tra chương trình với từ khóa 'void' không hợp lệ."""
    source = """void"""
    expected = "Error on line 1 col 0: void"
    assert Parser(source).parse() == expected

def test_239():
    """Kiểm tra chương trình với khai báo 'package' không hợp lệ."""
    source = """package main"""
    expected = "Error on line 1 col 0: package"
    assert Parser(source).parse() == expected

def test_240():
    """Kiểm tra chương trình với từ khóa 'switch' không hợp lệ."""
    source = """switch"""
    expected = "Error on line 1 col 0: switch"
    assert Parser(source).parse() == expected

def test_241():
    """Kiểm tra chương trình với định danh 'case' không hợp lệ."""
    source = """case"""
    expected = "Error on line 1 col 0: case"
    assert Parser(source).parse() == expected

def test_242():
    """Kiểm tra chương trình với định danh 'default' không hợp lệ."""
    source = """default"""
    expected = "Error on line 1 col 0: default"
    assert Parser(source).parse() == expected

def test_243():
    """Kiểm tra chương trình với định danh 'map' và cú pháp kiểu không hợp lệ."""
    source = """map[string]int"""
    expected = "Error on line 1 col 0: map"
    assert Parser(source).parse() == expected

def test_244():
    """Kiểm tra chương trình với định danh 'defer' không hợp lệ."""
    source = """defer"""
    expected = "Error on line 1 col 0: defer"
    assert Parser(source).parse() == expected

def test_245():
    """Kiểm tra chương trình với định danh 'go' không hợp lệ."""
    source = """go"""
    expected = "Error on line 1 col 0: go"
    assert Parser(source).parse() == expected

def test_246():
    """Kiểm tra chương trình với định danh 'interface' không hợp lệ."""
    source = """interface"""
    expected = "Error on line 1 col 0: interface"
    assert Parser(source).parse() == expected

def test_247():
    """Kiểm tra chương trình với định danh 'struct' và cú pháp kiểu không hợp lệ."""
    source = """struct"""
    expected = "Error on line 1 col 0: struct"
    assert Parser(source).parse() == expected

def test_248():
    """Kiểm tra chương trình với định danh 'chan' không hợp lệ."""
    source = """chan"""
    expected = "Error on line 1 col 0: chan"
    assert Parser(source).parse() == expected

def test_249():
    """Kiểm tra chương trình với định danh 'range' không hợp lệ."""
    source = """range"""
    expected = "Error on line 1 col 0: range"
    assert Parser(source).parse() == expected

def test_250():
    """Kiểm tra chương trình với định danh 'select' không hợp lệ."""
    source = """select"""
    expected = "Error on line 1 col 0: select"
    assert Parser(source).parse() == expected
def test_251():
    """Kiểm tra hàm main cơ bản với khai báo biến, if-else và trả về chuỗi (đã sửa để thành công)."""
    source = """
        func main() -> string {
            let a: int = 5;
            let b: float = 3.14;
            if (a > b) {
                return "Greater";
            } else {
                return "Smaller";
            }
        }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_252():
    """Kiểm tra khai báo biến/hằng toàn cục với từ khóa 'let' không hợp lệ và thiếu dấu hai chấm cho kiểu (vẫn là lỗi)."""
    source = """
            let x int = 10;
            const PI float = 3.1415;
            let name string = "John Doe";
            let isActive bool = true;
    """
    expected = "Error on line 2 col 12: let" # Lỗi đầu tiên là 'let' không hợp lệ ở cấp độ toàn cục
    assert Parser(source).parse() == expected

def test_253():
    """Kiểm tra câu lệnh if-else-if độc lập (không nằm trong hàm)."""
    source = """
            if (x > 5) {
                y = x * 2;
            } else if (x == 5) {
                y = x + 10;
            } else {
                y = 0;
            }
    """
    expected = "Error on line 2 col 12: if"
    assert Parser(source).parse() == expected

def test_254():
    """Kiểm tra câu lệnh vòng lặp for độc lập (không nằm trong hàm)."""
    source = """
        for (i = 0; i < 10; i = i + 1) {
            print(i);
        }
    """
    expected = "Error on line 2 col 8: for"
    assert Parser(source).parse() == expected

def test_255():
    """Kiểm tra khai báo hàm giai thừa đúng cú pháp (đã sửa để thành công)."""
    source = """
        func factorial(n: int) -> int {
            if (n == 0) {
                return 1;
            }
            return n * factorial(n - 1);
        }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_256():
    """Kiểm tra khai báo kiểu 'struct' và định nghĩa phương thức (không được hỗ trợ tường minh trong HLang)."""
    source = """
        type Person struct {
            name string;
            age int;
            func (p Person) GetAge() int {
                return p.age;
            }
        }
        """
    expected = "Error on line 2 col 8: type" # Cú pháp method receiver không được hỗ trợ tường minh
    assert Parser(source).parse() == expected

def test_257():
    """Kiểm tra khởi tạo mảng đa chiều với từ khóa 'let' và cú pháp kiểu mảng sai (vẫn là lỗi)."""
    source = """
        func main() -> void {
            let arr: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
        }
        """
    expected = "success" # Lỗi đầu tiên là 'let' không hợp lệ
    assert Parser(source).parse() == expected

def test_258():
    """Kiểm tra hàm với danh sách tham số và khai báo mảng đa chiều đúng cú pháp (đã sửa để thành công)."""
    source = """
        func myFunc(a: int, b: int, c: string) -> int {
            let arr: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
            return 0;
        }
        """
    expected = "success"
    assert Parser(source).parse() == expected

def test_259():
    """Kiểm tra hàm với danh sách tham số và khai báo mảng đa chiều có kiểu tường minh đúng cú pháp (đã sửa để thành công)."""
    source = """
        func myFunc(a: int, b: int, c: string) -> int {
            let arr: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
            return 0;
        };
        """
    expected = "success"
    assert Parser(source).parse() == expected

def test_260():
    """Kiểm tra hàm với danh sách tham số, khai báo mảng và trả về chuỗi đúng cú pháp (đã sửa để thành công)."""
    source = """
        func myFunc(a: int, b: int, c: string) -> string {
            let arr: [int; 5];
            return "Hello HLang";
        }
        """
    expected = "success"
    assert Parser(source).parse() == expected

def test_261():
    """Kiểm tra hàm với danh sách tham số không hợp lệ và khai báo biến không đầy đủ."""
    source = """
        func myFunc(a, b int, c string) [2]int {
            let arr;
        }
    """
    expected = "Error on line 2 col 21: ," # Tham số hàm phải có dấu hai chấm: b: int
    assert Parser(source).parse() == expected

def test_262():
    """Kiểm tra câu lệnh 'continue' độc lập (phải nằm trong vòng lặp)."""
    source = """
        continue;
    """
    expected = "Error on line 2 col 8: continue"
    assert Parser(source).parse() == expected

def test_263():
    """Kiểm tra câu lệnh biểu thức độc lập (phải nằm trong hàm)."""
    source = """
        x == 10;
    """
    expected = "Error on line 2 col 8: x"
    assert Parser(source).parse() == expected

def test_264():
    """Kiểm tra khai báo biến toàn cục với từ khóa 'let' không hợp lệ và thiếu toán tử gán."""
    source = """
    func main() -> void {
        let name string "Hello";
    }
    """
    expected = "Error on line 3 col 17: string"
    assert Parser(source).parse() == expected

def test_265():
    """Kiểm tra chuỗi không đóng (lỗi lexical)."""
    source = """
    func main() -> void {
        let str = "This is an unclosed string
        }
    """
    expected = "Unclosed String: This is an unclosed string"
    assert Parser(source).parse() == expected

def test_266():
    """Kiểm tra chuỗi với ký tự thoát không hợp lệ (lỗi lexical)."""
    source = """
    func main() -> void {
       let str = "Hello\\qWorld";
       }
    """
    expected = "Illegal Escape In String: Hello\\q"
    assert Parser(source).parse() == expected

def test_268():
    """Kiểm tra khai báo kiểu lồng nhau và định nghĩa phương thức (không được hỗ trợ trong HLang)."""
    source = """
        type Outer struct {
            type Inner struct {
                value int;
                func (i Inner) GetValue() int {
                    return i.value;
                }
            }
            inner Inner;
            func (o Outer) GetInnerValue() int {
                return o.inner.GetValue();
            }
        }
    """
    expected = "Error on line 2 col 8: type" # HLang không hỗ trợ khai báo kiểu lồng nhau
    assert Parser(source).parse() == expected

def test_270():
    """Kiểm tra khai báo kiểu bị sai cú pháp với từ khóa 'struct' và định nghĩa phương thức (vẫn là lỗi)."""
    source = """
        type ErrorStruct struct {
            name string;
            age int;
            func (e ErrorStruct) GetName() string {
                return e.name;
            };
        }
    """
    expected = "Error on line 2 col 8: type" # 'func' không được mong đợi ở vị trí này trong khai báo kiểu
    assert Parser(source).parse() == expected

def test_271():
    """Kiểm tra khai báo kiểu bị sai cú pháp (giống test_270)."""
    source = """
        type ErrorStruct struct {
            name string;
            age int;
            func (e ErrorStruct) GetName() string {
                return e.name;
            };
        }"""
    expected = "Error on line 2 col 8: type" # Lỗi tương tự như test_270
    assert Parser(source).parse() == expected

def test_272():
    """Kiểm tra khai báo kiểu không hợp lệ với từ khóa 'struct' và thiếu dấu hai chấm (đã sửa để báo lỗi)."""
    source = """
        type ErrorStruct struct {
            name string;
            age int;
            /*func (e ErrorStruct) GetName() string
                return e.name;
            };
            */
        }
    """
    expected = "Error on line 2 col 8: type" # HLang không hỗ trợ cú pháp struct như vậy, mong đợi ':' sau ID
    assert Parser(source).parse() == expected

def test_273():
    """Kiểm tra hàm Fibonacci với cú pháp đúng (đã sửa để thành công)."""
    source = """
        func Fibonacci(n: int) -> int {
            if (n <= 1) {
                return n;
            }
            let a: int = Fibonacci(n - 1) + Fibonacci(n - 2);
            return a;
        }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_274():
    """Kiểm tra câu lệnh vòng lặp for độc lập với continue và break (phải nằm trong hàm)."""
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
    expected = "Error on line 2 col 8: for"
    assert Parser(source).parse() == expected

def test_275():
    """Kiểm tra khai báo biến toàn cục với từ khóa 'let' không hợp lệ và kiểu không xác định (vẫn là lỗi)."""
    source = """
        let unknownType myCustomType = 10;
    """
    expected = "Error on line 2 col 8: let" # 'let' không phải là từ khóa khai báo biến ở cấp độ toàn cục
    assert Parser(source).parse() == expected

def test_277():
    """Kiểm tra khai báo biến toàn cục với từ khóa 'let' không hợp lệ và phép chia cho 0 (lỗi semantic/runtime)."""
    source = """
        let result float = 10 / 0;
    """
    expected = "Error on line 2 col 8: let" # 'let' không phải là từ khóa khai báo biến ở cấp độ toàn cục
    assert Parser(source).parse() == expected

def test_278():
    """Kiểm tra khai báo biến toàn cục với từ khóa 'let' không hợp lệ và không khớp kiểu (lỗi semantic)."""
    source = """
        let a int = "string_value";
    """
    expected = "Error on line 2 col 8: let" # 'let' không phải là từ khóa khai báo biến ở cấp độ toàn cục
    assert Parser(source).parse() == expected

def test_279():
    """Kiểm tra hàm trả về giá trị (đã sửa để thành công)."""
    source = """
        func NoReturn() -> int {
            return 0;
        }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_280():
    """Kiểm tra hàm với kiểu trả về không phải 'void' nhưng thân hàm rỗng."""
    source = """
        func NoReturn() -> int {
        }
    """
    expected = "success" # Trình phân tích cú pháp mong đợi một câu lệnh (như 'return') trước dấu '}'
    assert Parser(source).parse() == expected

def test_281():
    """Kiểm tra hàm với nhiều tham số và kiểu trả về đúng cú pháp (đã sửa để thành công)."""
    source = """
        func NoReturn(a: int, b: int, c: int, d: int, e: int, asd: float, trh6h: string) -> int {
            return 0;
        }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_282():
    """Kiểm tra câu lệnh if-else lồng nhau với cú pháp đúng (đã sửa để thành công)."""
    source = """
        func NestedIf(x: int) -> string {
            if (x > 0) {
                if (x > 10) {
                    return "Greater than 10";
                } else {
                    if (x == 5) {
                        return "Equal to 5";
                    } else {
                        return "Between 1 and 10";
                    }
                }
            } else {
                return "Negative";
            }
        }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_283():
    """Kiểm tra khai báo hàm thiếu dấu ngoặc nhọn cho thân hàm."""
    source = """
        func MissingBrace() -> int return 10;
    """
    expected = "Error on line 2 col 35: return" # Trình phân tích cú pháp mong đợi '{' sau khai báo hàm, không phải 'return'
    assert Parser(source).parse() == expected

def test_284():
    """Kiểm tra hàm có kiểu trả về nhưng thân hàm rỗng."""
    source = """
        func NoReturnValue() -> string {
        }
    """
    expected = "success" # Trình phân tích cú pháp mong đợi một câu lệnh (như 'return') trước dấu '}'
    assert Parser(source).parse() == expected

def test_285():
    """Kiểm tra gán giá trị cho biến chưa khai báo (lỗi semantic, nhưng cú pháp đúng)."""
    source = """
        func UndefinedVariable() -> void {
            x = 10;
        }
    """
    expected = "success" # Cú pháp của câu lệnh gán là hợp lệ
    assert Parser(source).parse() == expected

def test_286():
    """Kiểm tra khai báo kiểu không hợp lệ với từ khóa 'struct' (vẫn là lỗi)."""
    source = """
        type InvalidStruct struct {
            name: string;
            age: unknownType;
        }
    """
    expected = "Error on line 2 col 8: type" # HLang không hỗ trợ cú pháp 'struct' như vậy, mong đợi ':' sau ID
    assert Parser(source).parse() == expected

def test_289():
    """Kiểm tra hàm với danh sách tham số không hợp lệ (thiếu dấu phẩy và dấu hai chấm)."""
    source = """
        func InvalidParams(x: int, y: string z: float) -> void {
            return;
        }
    """
    expected = "Error on line 2 col 45: z" # Trình phân tích cú pháp mong đợi dấu phẩy hoặc ')' sau 'y: string'
    assert Parser(source).parse() == expected

def test_290():
    """Kiểm tra khai báo kiểu không hợp lệ với từ khóa 'struct' và trường trùng lặp (vẫn là lỗi)."""
    source = """
        type DuplicateField struct {
            name: string;
            name: int;
        }
    """
    expected = "Error on line 2 col 8: type" # HLang không hỗ trợ cú pháp 'struct' như vậy
    assert Parser(source).parse() == expected

def test_292():
    """Kiểm tra khai báo biến với ký tự không hợp lệ trong biểu thức (lỗi lexical)."""
    source = """
    func main() -> void {
        let specialVar = @#$%^&*();
        }
    """
    expected = "Error Token @" # Ký tự '@' không hợp lệ
    assert Parser(source).parse() == expected

def test_293():
    """Kiểm tra định nghĩa hàm lồng nhau (không được hỗ trợ trong HLang)."""
    source = """
        func Outer() -> void {
            func Inner() -> void {
                print("Inner function");
            }
            Inner();
        }
    """
    expected = "success" # HLang không hỗ trợ định nghĩa hàm lồng nhau
    assert Parser(source).parse() == expected

def test_294():
    """Kiểm tra khai báo mảng toàn cục với cú pháp kiểu mảng sai."""
    source = """
    func main() -> void {
        let arr: [int; 5] = [1, 2, 3, 4, 5];
        }
    """
    expected = "success" # Đã sửa cú pháp mảng và khai báo 'let'
    assert Parser(source).parse() == expected

def test_295():
    """Kiểm tra chương trình rỗng (không hợp lệ)."""
    source = """
        
    """
    expected = "Error on line 3 col 4: <EOF>" # Chương trình HLang yêu cầu ít nhất một hàm main
    assert Parser(source).parse() == expected

def test_296():
    """Kiểm tra định danh 'nil' độc lập (không hợp lệ làm chương trình)."""
    source = """
        nil
    """
    expected = "Error on line 2 col 8: nil"
    assert Parser(source).parse() == expected

def test_297():
    """Kiểm tra chương trình chỉ gồm comment và định danh (không hợp lệ)."""
    source = """
        /* test
    */ a /* */
    """
    expected = "Error on line 3 col 7: a" # Trình phân tích cú pháp mong đợi cấu trúc chương trình hợp lệ, không phải định danh 'a'
    assert Parser(source).parse() == expected

def test_298():
    """Kiểm tra khai báo kiểu không hợp lệ với 'struct', cú pháp phương thức không hỗ trợ và khai báo trường sai."""
    source = """
        type Person struct {
            func (p Person) Greet() string {
                return "Hello, " + p.name;
            };
            c: c_type; // Sửa lỗi khai báo trường
            func (p Person) Greet() string {
                return "Hello, " + p.name;
            };
        }
    """
    expected = "Error on line 2 col 8: type" # Lỗi đầu tiên là cú pháp 'type ID struct {' không hợp lệ
    assert Parser(source).parse() == expected

def test_299():
    """Kiểm tra cú pháp khai báo phương thức không được hỗ trợ với cấu trúc if-else."""
    source = """
        func (p Person) Greet() -> string {
            if (true) {return "Hello";};
            else if (false) {return "Bye";};
        };
    """
    expected = "Error on line 2 col 13: (" # Cú pháp phương thức '(p Person)' không hợp lệ cho khai báo hàm cấp cao nhất
    assert Parser(source).parse() == expected

def test_300():
    """Kiểm tra khai báo kiểu không hợp lệ với 'struct', trường sai cú pháp và phương thức không hỗ trợ."""
    source = """
        type Person struct {
            /* func (p Person) Greet() string {
                return "Hello, " + p.name
            }
            */
            c: c_type; // Sửa lỗi khai báo trường
            func (c c_type) Add(x: int, y: int, b: float) -> void {return ;};
            value: int;
        }
    """
    expected = "Error on line 2 col 8: type" # Lỗi đầu tiên là cú pháp 'type ID struct {' không hợp lệ
    assert Parser(source).parse() == expected

def test_001():
    """Test basic function declaration"""
    source = 'func main() -> void {}'
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Test function with parameters"""
    source = 'func add(a: int, b: int) -> int { return a + b; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_003():
    """Test variable declaration with type annotation"""
    source = 'func main() -> void { let x: int = 42; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_004():
    """Test variable declaration with type inference"""
    source = 'func main() -> void { let name = "Alice"; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_005():
    """Test constant declaration"""
    source = 'const PI: float = 3.14159; func main() -> void {}'
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
}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_007():
    """Test while loop"""
    source = """func main() -> void {
    let i = 0;
    while (i < 10) {
        i = i + 1;
    }
}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_008():
    """Test for loop with array"""
    source = """func main() -> void {
    let numbers = [1, 2, 3, 4, 5];
    for (num in numbers) {
        print(str(num));
    }
}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_009():
    """Test array declaration and access"""
    source = """func main() -> void {
    let arr: [int; 3] = [1, 2, 3];
    let first = arr[0];
    arr[1] = 42;
}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_010():
    """Test complex expression with pipeline operator"""
    source = """func main() -> void {
    let result = data >> process >> validate >> transform;
    let calculation = 5 >> add(3) >> multiply(2);
}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_011():
    """Test parser error: missing closing brace in function declaration"""
    source = 'func main() -> void { let x = 1; '
    expected = "Error on line 1 col 33: <EOF>"
    assert Parser(source).parse() == expected

def test_012():
    """Test const declaration"""
    source = 'const MAX_VALUE: int = 100;'
    expected = "success"
    assert Parser(source).parse() == expected

def test_016():
    """Test empty array literal"""
    source = 'const a = [];'
    expected = "success"
    assert Parser(source).parse() == expected

def test_047():
    """Test unary minus with multiplication"""
    source = 'const votien = a * -b;'
    expected = "success"
    assert Parser(source).parse() == expected

def test_053():
    """Test complex sequence of unary and postfix operators"""
    source = 'const votien = !"s" + !!!b --!+!-c;'
    expected = "success"
    assert Parser(source).parse() == expected

def test_058():
    """Test indexing and mixed expressions"""
    source = 'const hung = a[1] + a[1+1] + c["s" * c];'
    expected = "success"
    assert Parser(source).parse() == expected

def test_060():
    """Test chained indexing"""
    source = 'const votien = [1, 2][2][2+2][3];'
    expected = "success"
    assert Parser(source).parse() == expected

def test_061():
    """Test parentheses with indexing"""
    source = 'const votien = (1+2)*3 + (a)[2][3];'
    expected = "success"
    assert Parser(source).parse() == expected

def test_063():
    """Test error on invalid multi-index syntax"""
    source = 'const votien = a[1, 2];'
    expected = "Error on line 1 col 18: ,"
    assert Parser(source).parse() == expected

def test_064():
    """Test mixed function calls and pipeline in expressions"""
    source = 'const votien = foo() + foo(1, 2) + foo(a[2], b >> c * 2);'
    expected = "success"
    assert Parser(source).parse() == expected

def test_066():
    """Test various function calls including built-ins"""
    source = ('const votien = str() + int(2, 3) + int(2) + int() + '
              'float() + float(true * 2); func main() -> void {}')
    expected = "success"
    assert Parser(source).parse() == expected

def test_083():
    """Test multiple function declarations"""
    source = """func f1() -> void {}
func f2(a: int) -> int {}
func f3(x: int, y: float, z: string) -> string {}
func f4(arr: [int; 3]) -> [int; 3] {}
func f5() -> bool {}
func f6() -> float {}
func empty() -> int {}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_117():
    """Test for-loops with invalid 'in' targets"""
    source = """func main() -> void {
    for (a in 1){}
    for (a in foo + foo()){}
}"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_118():
    """Test for-loops with invalid 'in' targets"""
    source = """func main() -> void { 
        let result = data >> process;
    };"""
    expected = "success"
    assert Parser(source).parse() == expected
