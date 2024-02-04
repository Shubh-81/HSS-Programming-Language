# H**

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    - [Hello, World!](#hello-world)
3. [Basic Syntax](#basic-syntax)
    - [Variables and Assignment](#variables-and-assignment)
    - [Basic Types](#basic-types)
    - [Compound Types](#compound-types)
    - [Conditionals](#conditionals)
    - [Loops](#loops)
4. [Functions and Closures](#functions-and-closures)
    - [Function Definition](#function-definition)
    - [Function Invocation](#function-invocation)
    - [Closures](#closures)
5. [Exception Handling](#exception-handling)
6. [Printing](#printing)
7. [Additional Features](#additional-features)
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

### Variables and Assignment
H** has two types of variable declaration.

**`var`**: Declares a variable and optionally initializes its value.

**`const`**: Declares a read-only named constant.

H** is a case-sensitive language. A H** identifier can start with a letter(a - z, A - Z) or with a underscore (_) and following characters can also include numbers (0 - 9). 

```python
const x = 5;              // Constant Variable
var y = 10;               // Non-Constant Variable

// Mutable variable assignment
y = 15;

// Multiple assignments
var a, b = 2, 3;
```

### Basic Types

H** is a **`dynamically`** typed programming language. This means that you do not need to declare the data type of a variable when you initialize it. The data type is determined automatically at runtime.

```python
var num = 42;            // Number
var isTrue = true;       // Boolean
var text = "Hello";      // String
var num = null           // null 
```

### Compound Types

There are three types of compound data types in H**.

**`tuple`**:  An immutable collection of objects. Can contain objects belonging to different data types.

**`list`**: A mutable collection of object of the same data type.

**`arr`**: A mutable collection of variable length (new items can be added using .append() method) containing objects of same data type.

```python
tuple t = [1, "two", true];      // Tuple
list l = [1, 2, 3, 4];           // List
arr a = [1, 2, 3, 4];            // Arr
```

### Conditionals

The conditionals in H** include **`if`**, **`elif`** and **`else`**. 
The H** conditionals are similar to Java conditionals.

```python
if (condition) {
    // code block
} elif (condition) {
    // code block
} else {
    // code block
}
```

### Loops
```python
while (condition) {
    // code block
}

for (var i = 0; i < 5; i++) {
    // code block
}

do {
    // code block
} while (condition)
```

## Functions and Closures

### Function Definition
```python
// Function definition
func add(var x, var y) {
    return x + y;
}
```

### Function Invocation
```python
// Function call
var result = add(3, 4);
```

### Closures
```python
func outerFunction() {
    var outerVar = "I'm from outer!";

    function innerFunction() {
        print(outerVar);
    }

    return innerFunction;
}

// Creating a closure
var closure = outerFunction();

// Executing the closure
closure();  // Outputs: I'm from outer!
```

## Exception Handling
```python
try {
    // code block
} catch (ExceptionType e) {
    // handle exception
} finally {
    // optional: code block to execute regardless of exception
}

throw ExceptionType("An error occurred");
```

## Printing
```python
print("Hello, World!");
```

## Additional Features

### Unary and Binary Operators
```python
var a = 5;
a++;
print(a); // Outputs 6
a+=1;
print(a) // Outputs 7
var b = 5
a = a + b
print(a) // Outputs 12
```

### Boolean Type
```python
var a = false;
if (!a) {
  print("Hello");    // Prints Hello
}
```

### Comparators and if-else
```python
if (a >= c) {
  print("Hello");
} elif (a == c) {
  print("World");
} else (a != c) {
  print("Worlds");
}
```

### Strings
```python
// Concatenation
var a = "Hello";
var b = "World";
var c = a + " " + b;
print(c); // Outputs "Hello World"

// Slicing
var a = "Hello World";
var c = a.slice(0, 5);
print(c); // Outputs "Hello"
```

### List and Arrays
```python
list l = [2, 3, 4];
l.append(5);
print(l[3]); // Outputs 5, list is variable in size

arr a = [2, 3, 4];
a.append(5); // Throws an error, array is fixed size

print(a.length()); // Outputs 3, same for list
print(a[0]);  // Prints first element, same for list
print(a[a.length() - 1]); // Prints last element, same for list
```

### Assignment and Let Expressions
```python
const a = 5; // Variable a cannot be changed after assignment
var b = 5; // Variable can be changed after assignment
```

