from lark import Lark, Tree
import sys
from lexer import Lexer as Lexer_
from lark.lexer import Lexer, Token

grammar = """
?start: statements

statements: statement+
statement: print | declare | exception_handling | return_statement | control | expression_statement

print: PRINT_KEYWORD ROUND_OPEN print_args ROUND_CLOSE END_OF_STATEMENT
print_args: expression (COMMA expression)* | 

expression_statement: expression END_OF_STATEMENT 
                    | assignment END_OF_STATEMENT

expression: expression OPERATOR expression -> binary_op 
 | expression COMPARATOR expression -> binary_comp
 | unary_expression 
 | function_call 
 | IDENTIFIER 
 | IDENTIFIER index
 | ROUND_OPEN expression ROUND_CLOSE 
 | literal 
 | IDENTIFIER COMPOUND_OPERATOR expression  -> binary_compound_op
 | IDENTIFIER DOT_OPERATOR IDENTIFIER expression -> binary_dot_op

unary_expression: UNARY_OPERATOR IDENTIFIER 
| IDENTIFIER UNARY_OPERATOR 
| NOT_OPERATOR IDENTIFIER 
| NOT_OPERATOR ROUND_OPEN expression ROUND_CLOSE

assignment: IDENTIFIER ASSIGNMENT_OPERATOR expression 

index: (SQUARE_OPEN expression SQUARE_CLOSE)+ 

control: function | if_else | while_ | do_while | for_loop | break_continue
function: FUNCTION_DECLARATION IDENTIFIER ROUND_OPEN parameters ROUND_CLOSE block
if_else: IF_ELIF ROUND_OPEN expression ROUND_CLOSE block else_temp 
else_temp: ELSE_KEYWORD block | 
while_: WHILE_KEYWORD ROUND_OPEN expression ROUND_CLOSE block
do_while: DO_KEYWORD block WHILE_KEYWORD ROUND_OPEN expression ROUND_CLOSE
for_loop: FOR_KEYWORD ROUND_OPEN dec_control_flow END_OF_STATEMENT expression END_OF_STATEMENT for_update ROUND_CLOSE block
for_update: expression | assignment
break_continue: BREAK_CONTINUE END_OF_STATEMENT

dec_control_flow: VARIABLE_DECLARATION IDENTIFIER ASSIGNMENT_OPERATOR expression

declare: tuple_declaration | list_declaration | arr_declaration | exception_declaration | variable_declaration 
tuple_declaration: TUPLE_DECLARATION IDENTIFIER ASSIGNMENT_OPERATOR matrix END_OF_STATEMENT
list_declaration: LIST_DECLARATION IDENTIFIER ASSIGNMENT_OPERATOR matrix END_OF_STATEMENT
arr_declaration: ARR_DECLARATION IDENTIFIER ASSIGNMENT_OPERATOR matrix END_OF_STATEMENT
exception_declaration: EXCEPTION_TYPE IDENTIFIER ASSIGNMENT_OPERATOR IDENTIFIER END_OF_STATEMENT
variable_declaration: VARIABLE_DECLARATION IDENTIFIER (COMMA IDENTIFIER)* ASSIGNMENT_OPERATOR expression (COMMA expression)* END_OF_STATEMENT

matrix: matrix_temp | list_content
matrix_temp: SQUARE_OPEN matrix (COMMA matrix)* SQUARE_CLOSE | 
list_content: SQUARE_OPEN expression (COMMA expression)* SQUARE_CLOSE | SQUARE_OPEN SQUARE_CLOSE

exception_handling: try_catch_finally | throw
try_catch_finally: TRY_KEYWORD block CATCH_KEYWORD ROUND_OPEN EXCEPTION_TYPE IDENTIFIER ROUND_CLOSE block FINALLY_KEYWORD block
throw: THROW_KEYWORD EXCEPTION_TYPE ROUND_OPEN print_args ROUND_CLOSE END_OF_STATEMENT

block: CURLY_OPEN statements CURLY_CLOSE | CURLY_OPEN CURLY_CLOSE

function_call: IDENTIFIER ROUND_OPEN argument_temp ROUND_CLOSE -> function_call 
| IDENTIFIER DOT_OPERATOR IDENTIFIER ROUND_OPEN argument_temp ROUND_CLOSE -> inbuilt_function_call

return_statement: RETURN_KEYWORD expression? END_OF_STATEMENT

literal: INTEGER_CONSTANT | DECIMAL_CONSTANT | STRING_LITERAL | BOOLEAN_VALUE | NULL_KEYWORD

argument_temp: expression (COMMA expression)* |

parameters: parameter (COMMA parameter)* |
parameter: VARIABLE_DECLARATION IDENTIFIER | LIST_DECLARATION IDENTIFIER | ARR_DECLARATION IDENTIFIER | TUPLE_DECLARATION IDENTIFIER

%declare STRING_LITERAL BOOLEAN_VALUE COMMA FUNCTION_DECLARATION BREAK_CONTINUE IF_ELIF ELSE_KEYWORD WHILE_KEYWORD DO_KEYWORD FOR_KEYWORD PRINT_KEYWORD RETURN_KEYWORD VARIABLE_DECLARATION LIST_DECLARATION ARR_DECLARATION TUPLE_DECLARATION EXCEPTION_TYPE NULL_KEYWORD TRY_KEYWORD CATCH_KEYWORD FINALLY_KEYWORD THROW_KEYWORD KEYWORD NOT_OPERATOR ASSIGNMENT_OPERATOR OPERATOR COMPOUND_OPERATOR UNARY_OPERATOR COMPARATOR DOT_OPERATOR PUNCTUATION END_OF_STATEMENT ROUND_OPEN ROUND_CLOSE CURLY_OPEN CURLY_CLOSE SQUARE_OPEN SQUARE_CLOSE DECIMAL_CONSTANT INTEGER_CONSTANT IDENTIFIER QUOTATION ERROR
%import common.WS
%ignore WS
"""

class MyLexer(Lexer):
    def __init__(self, lexer_conf):
        pass

    def lex(self, data):
        lexer = Lexer_(source_code=data)
        lexer.tokenize()
        tokens = lexer.get_tokens()
        for type, value in tokens:
            yield Token(type, value)


parser = Lark(grammar, start='start', lexer=MyLexer)

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