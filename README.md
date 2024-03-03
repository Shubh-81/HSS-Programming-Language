# H**

## Table of Contents
- [H\*\*](#h)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Getting Started](#getting-started)
    - [Hello, World!](#hello-world)
  - [Basic Syntax](#basic-syntax)
    - [Keywords](#keywords)
    - [Variables and Assignment](#variables-and-assignment)
    - [Basic Types](#basic-types)
    - [Compound Types](#compound-types)
    - [Conditionals](#conditionals)
    - [Loops](#loops)
  - [Functions and Closures](#functions-and-closures)
    - [Function Definition](#function-definition)
    - [Function Invocation](#function-invocation)
    - [Closures](#closures)
  - [Exception Handling](#exception-handling)
  - [Printing](#printing)
  - [Additional Features](#additional-features)
    - [Unary and Binary Operators](#unary-and-binary-operators)
    - [Boolean Type](#boolean-type)
    - [Comparators and if-else](#comparators-and-if-else)
    - [Strings](#strings)
    - [List and Arrays](#list-and-arrays)
    - [Assignment and Let Expressions](#assignment-and-let-expressions)

## Introduction
H** is a minimalistic imperative programming language designed for simplicity and ease of use. It incorporates basic types, compound types, conditionals, loops, functions, closures, mutable variables, exceptions, and more.

**Group Name:** Dominance

**Members:**
- Shubh Agarwal
- Pulkit Gautam
- Manav Parmar
- Aman Singh

## Getting Started

### Hello, World!
```python
print("Hello, World!");
```

## Basic Syntax

### Keywords

H** has a set of keywords defined that can't be used as identifiers. 

| Keyword | Description |
| --- | --- |
| arr | mutable collection of fixed length |
| break | terminates a loop |
| catch | catches an exception during execution|
| const | identifier for constant value |
| continue | skips the iteration |
| do | do-while loops |
| elif | conditional statement |
| else | conditional statement |
| false | boolean |
| finally | runs the code block irrespective of the exceptions |
| for | iterate for some fixed number |
| func | define a function |
| if | conditional statement |
| list | mutable collections with variable length |
| null | denotes null value |
| print | returns the ouput to stdout | 
| return | returns output of a function |
| this | scope variable| 
| throw | throws an exception |
| true | boolean |
| try | error handling |
| tuple | immutable collection of objects |
| typeof | returns the data type |
| var | identifier for mutable object |
| while | iterate till a certain condition is met |




### Variables and Assignment
H** has two types of variable declaration.

**`var`**: Declares a variable and optionally initializes its value.

**`const`**: Declares a read-only named constant.

H** is a case-sensitive language. A H** identifier can start with a letter(a - z, A - Z) or with a underscore (_) and following characters can also include numbers (0 - 9). 

```python
const x = 5;              /* Constant Variable */
var y = 10;               /* Non-Constant Variable */

/* Mutable variable assignment */
y = 15;

/* Multiple assignments */
var a, b = 2, 3;
```

### Basic Types

H** is a **`dynamically`** typed programming language. This means that you do not need to declare the data type of a variable when you initialize it. The data type is determined automatically at runtime.

```python
var num = 42;            /* Number */
var isTrue = true;       /* Boolean */
var text = "Hello";      /* String */
var num = null           /* null */ 
```

### Compound Types

There are three types of compound data types in H**.

**`tuple`**:  An immutable collection of objects. Can contain objects belonging to different data types.

**`list`**: A mutable collection of variable length (new items can be added using .append() method) containing objects of same data type.

**`arr`**: A mutable collection of object of the same data type.

```python
tuple t = [1, "two", true];      /* Tuple */
list l = [1, 2, 3, 4];           /* List */
arr a = [1, 2, 3, 4];           /* Arr */
```

### Conditionals

The conditionals in H** include **`if`**, **`elif`** and **`else`**. 
The H** conditionals are similar to Java conditionals.

```python
if (condition) {
    /* code block */
} elif (condition) {
   /* code block */
} else {
    /* code block */
}
```

### Loops

H** has three kind of loops namely 'while', 'for' and 'do while'. 

**`while`** - Here loop checks the condition first, if it would pass then run the code inside the '{  //code }' brackets.
again come to the top ,check the codition and so on till condition fails.

**`for`** - Here we have three terms in initial bracket separated by two semi colon.
first term - we declare and initialise a variable(let i) 
second term - we check the condition based on declared variable, if pass then go to loop 
third term - after running code inside the loop, we first return to the third term and do the mentioned operation on the variable and again check the condition mentioned on the second term and do the same as before till condition satisfied of the 
second term 

**`do while`** - Here we first run the code inside the 'do' loop and then check the condition inside the 'while' if passed then 
again do the same till condition fails.


```python
while (condition) {
    /* code block */
}

for (var i = 0; i < 5; i++) {
    /* code block */
}

do {
    /* code block */
} while (condition)
```

## Functions and Closures

### Function Definition

**`func`** takes 0 or more argument and return values based on the code written in it.
we first write keyword **`func`**, then name of our function we want to assign, arguments inside '()', and run the code inside 
'{ }'. 

```python
/* Function definition */
func add(var x, var y) {
    return x + y;
}
```

### Function Invocation

Below is the method to call a function. The returned value of the function can be stored as new variable. 
if there is no return in the function then we only have to call the function (eg. bfs(ad, 4))
```python
/* Function call */
var result = add(3, 4);
```

### Closures

A variable may belong to one of these 3 scopes in H**.

**`Global Scope`**: The default scope for all code running in script mode.

**`Function Scope`**: The scope created with a function (inside {}).

Variables declared outside of any function in H** are known as **`global`** variables. They are called global because they are accessible to any other code in the same document. On the other hand, variables declared inside a function are known as **`local`** variables. Local variables are only available within the scope of that particular function. Unlike global variables, local variables cannot be accessed outside of the block they are declared in. This difference in scope access is the key distinction between global and local variables in H**.

```python
func outerFunction() {
    var outerVar = "I'm from outer!";

    func innerFunction() {
        print(outerVar);
    }

    return innerFunction;
}

/* Creating a closure */
var closure = outerFunction();

/* Executing the closure */
closure();  /* Outputs: I'm from outer! */
``` 

## Exception Handling

The **`try...catch`** statement in H** allows you to define a block of code to execute (the try block), and to define custom behavior in case there are exceptions while running that code (the catch block). When code within the try block throws an exception, execution is immediately shifted to the catch block, bypassing any remaining statements in the try block. 
It is important to note that **`finally`** block will execute whether or not an exception is thrown. You may use **`finally`** to release the resources tied up to your script.

```python
try {
    /* code block */
} catch (ExceptionType e) {
    /* handle exception */
} finally {
   /* optional: code block to execute regardless of exception */
}

throw ExceptionType("An error occurred");
```

## Printing
To print any string we write inside double inverted comma (" ") and use keyword **`print`**.
```python
print("Hello, World!");
```

## Additional Features

### Unary and Binary Operators

In (a = a + b) we first calculate right side of equivalent '=' and then assign the resultant value to the left side. 
a++ is equivalent to a = a+1 , but if we pass 'a++' as an argument then a will be passed not a+1
a+=b is equivalent to a = a+b.

```python
var a = 5;
a++;
print(a); /*  Outputs 6 */
a+=1;
print(a) /* Outputs 7 */
var b = 5
a = a + b
print(a) /* Outputs 12 */
```

### Boolean Type

Boolean value is also included in var variable.
There will be two values for boolean variable - **`true`**  and  **`false`**.

In condition we'll check if the value is **`true`** or **`false`** and proceed accordingly.

```python
var a = false;
if (!a) {
  print("Hello");    /* Prints Hello */
}
```

### Comparators and if-else

The comparators return a boolean value. If the relation is valid then it returns true otherwise false.
like in (a >= c) if a is greater or equal to c then return true otherwise false.
In (a <= c) if a is lesser or equal to c then return true otherwise false
In (a == c)if a is equal to c then return true otherwise false
if (a != c)if a is not equal to c then return true otherwise false

```python
if (a >= c) {
  print("Hello");
} elif (a == c) {
  print("World");
} else{
  print("Worlds");
}
```

### Strings

We can declare string using **`var`** or **`const`** keywords.
String can be added using '+' sign. We can give the string itself or variable which contained the string for addition.
Addition of string 'a + b' signifies that, after last character of string a we will have first character of string b and 
total string will end on last character of string b.

We use slice function if we want a substring of a string. 
a.slice(i, l) signfies that we want a substring which start from the index i of string a and have a length of l.

```python
/* Concatenation */
var a = "Hello";
var b = "World";
var c = a + " " + b;
print(c); /* Outputs "Hello World" */

/* Slicing */
var a = "Hello World";
var c = a.slice(0, 5);
print(c); /* Outputs "Hello" */
```

### List and Arrays

```python
list l = [2, 3, 4];
l.append(5);
print(l[3]); /* Outputs 5, list is variable in size */

arr a = [2, 3, 4];
a.append(5); /* Throws an error, array is fixed size */

print(a.length()); /* Outputs 3, same for list */
print(a[0]);  /* Prints first element, same for list */
print(a[a.length() - 1]); /* Prints last element, same for list */
```

### Assignment and Let Expressions
**`const`**: Assigns an indentifier to a constant value.

**`var`**: Declares a variable and optionally initializes its value.
```python


const a = 5; /* Variable a cannot be changed after assignment */
var b = 5; /* Variable can be changed after assignment */
```

## Lexer

Test cases are present in the `testcases` folder with the extension `.hss`.

To run the lexer, use the following command:

```bash
python lexer.py <path_to_testcase.hss>
```
