from lark import Lark, Tree
import sys

grammar = """
    start: statements

    statements: statement+

    statement: expression ";" 
             | assignment ";" 
             | control_flow 
             | declaration ";" 
             | return_statement ";" 
             | exception_handling 
             | print_statement ";"
             | comments 

    comments: "/*" comment_text? "*/"

    comment_text: comment_char*

    comment_char: /[^\\n]/ | /\\n/

    expression: expression operator operand
              | expression operator identifier "[" (identifier | integer_constant | expression) "]"
              | expression comparator (operand | function_call)
              | operand operator
              | operand
              | function_call
              | "!" BOOLEAN_VAR
              | identifier "[" (identifier | integer_constant) "]"
              | BOOLEAN_VAR
              | function_call operator operand
              | identifier "[" (identifier | integer_constant| expression)"]"
              | identifier "[" (identifier | integer_constant| expression)"]" operand expression

    assignment: "var" identifier ("," identifier)* "=" (literal | identifier | expression) ("," literal | identifier | expression)*
              | "const" identifier ("," identifier)* "=" (literal | identifier | expression) ("," literal | identifier | expression)*
              | identifier "[" (integer_constant | identifier) "]" "=" expression
              | identifier ("," identifier)* "=" (literal | identifier | expression) ("," literal | identifier | expression)*
              | identifier index "=" expression

    index:     "[" (expression | integer_constant) "]" 
              | index "[" (expression |integer_constant) "]"
              
    control_flow: "func" identifier "(" parameters ")" block
                |"if" "(" expression ")" block
                | "elif" "(" expression ")" block
                | "else" block
                | "while" "(" expression ")" block
                | "do" block "while" "(" expression ")" 
                | "for" "(" assignment ";" expression ";" (expression | assignment) ")" block
                | "break" ";"
                | "continue" ";"

    declaration: "tuple" identifier "=" "[" expression ("," expression)* "]"
                | "list" identifier "=" "[" expression ("," expression)* "]"
                | "list" identifier "=" "[" ("," | (expression))* "]"
                | "arr" identifier "=" "[" literal ("," literal)* "]"
                | "ExceptionType" identifier "=" identifier
                | "null" ";"
                | "list" identifier "=" matrix
    
    matrix : "[" [items]"]"

    items: value ("," value)*
    value: matrix | literal

    exception_handling: "try" block "catch" "(" "ExceptionType" identifier ")" block "finally" block
                       | "throw" "ExceptionType" "(" comment_text ")" ";"

    print_statement: "print" "(" (expression) ")"

    block: "{" statements "}" | "{" "}"

    function_call: identifier "(" arguments ")"
    | identifier "." identifier "(" arguments ")" 


    operand: identifier
           | literal

    return_statement: "return" (expression)

    operator: "+"
            | "-"
            | "*"
            | "/"
            | "%"
            | "+="
            | "-="
            | "++"
            | "--"
            | "&"
            | "|"

    comparator: "=="
              | "!="
              | "<=" 
              | ">="
              | "<"
              | ">"
              | "||"
              | "&&"

    identifier: /[a-zA-Z_][a-zA-Z0-9_]*/

    literal: integer_constant
           | decimal_constant
           | string_literal
           | BOOLEAN_VAR
           | "!" (BOOLEAN_VAR | identifier)

    BOOLEAN_VAR: "true" | "false"

    integer_constant: /[0-9]+/

    decimal_constant: /[0-9]+ '.' [0-9]+/

    string_literal: /"[^"]*"/

    arguments: ("," | expression)*

    parameters: parameter ("," parameter)*
                | ("," expression)*

    parameter: "var" identifier | "const" identifier

    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, start='start')

input_string = """

 
list a =[[1,2,3],[2,3,4],[2,3,4]];
list a=[[[[[]]]]];
a[1][2][3]=11;

 
"""

def visualize_tree(tree, depth=0):
    if isinstance(tree, Tree):
        print("  " * depth + "+-" + str(tree.data))
        for child in tree.children[:-1]:
            print("  " * (depth + 1) + "|")
            visualize_tree(child, depth + 1)
        if tree.children:
            print("  " * (depth + 1) + "|")
            visualize_tree(tree.children[-1], depth + 1)
    else:
        print("  " * depth + "+-" + str(tree))

try:
    tree = parser.parse(input_string)
    visualize_tree(tree)
    print("Parsing successful.")
except Exception as e:
    print("Parsing failed:", e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parsing.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        source_code = file.read()
    try:
        tree = parser.parse(source_code)
        print("Parsing successful.")
    except Exception as e:
        print("Parsing failed:", e)
        sys.exit(1)