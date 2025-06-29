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
def test_034():
    """Test complex expression with pipeline operator"""
    source = """let age: int = 25;                    // Explicit type annotation
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


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_035():
    """Test complex expression with pipeline operator"""
    source = """// Variable assignment:
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


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_036():
    """Test complex expression with pipeline operator"""
    source = """// Simple if statement:
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


"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_037():
    """Test complex expression with pipeline operator"""
    source = """// Basic counting loop:
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



"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_038():
    """Test complex expression with pipeline operator"""
    source = """// Array iteration:
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

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_039():
    """Test complex expression with pipeline operator"""
    source = """// Early loop termination:
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

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_040():
    """Test complex expression with pipeline operator"""
    source = """// Skip even numbers:
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

// Non-void function return:
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
    source = """func modifyInt(x: int) -> void {
    x = 100;  // Only modifies local parameter copy
}

let value = 42;
modifyInt(value);
// value is still 42 after function call

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_046():
    """Test complex expression with pipeline operator"""
    source = """func processString(text: string) -> string {
    // Cannot modify text parameter directly
    return text + " processed";
}

let original = "data";
let result = processString(original);
// original remains "data", result is "data processed"

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_047():
    """Test complex expression with pipeline operator"""
    source = """func fillArray(arr: [int; 3], value: int) -> void {
    for (i in [0, 1, 2]) {
        arr[i] = value;  // Modifies original array
    }
}

let numbers = [1, 2, 3];
fillArray(numbers, 99);
// numbers is now [99, 99, 99]

"""
    expected = "success"
    assert Parser(source).parse() == expected
def test_048():
    """Test complex expression with pipeline operator"""
    source = """let globalConst = 100;  // Global scope

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
        return 1;                    // Base case
    }
    return n * factorial(n - 1);     // Recursive call
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
    source = """// String conversion examples:
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
def test_056():
    """Test complex expression with pipeline operator"""
    source = """abc
"""
    expected = "success"
    assert Parser(source).parse() == expected
