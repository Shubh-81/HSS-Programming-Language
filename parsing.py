from lark import Lark, Tree
import sys
from lexer import Lexer as Lexer_
from lark.lexer import Lexer, Token

grammar = """
    start: statements

    statements: statement+

    statement: print_statement END_OF_STATEMENT
             | declaration END_OF_STATEMENT 
             | exception_handling 
             | return_statement END_OF_STATEMENT
             | control_flow 
             | expression END_OF_STATEMENT 
             | assignment END_OF_STATEMENT               

    print_statement: PRINT_KEYWORD ROUND_OPEN (expression | literal | identifier) (COMMA(expression | literal | identifier))* ROUND_CLOSE

    expression: expression operator operand
              | expression operator identifier SQUARE_OPEN (identifier | integer_constant | expression) SQUARE_CLOSE
              | expression comparator expression
              | operand unary_operator
              | operand
              | function_call
              | NOT_OPERATOR(BOOLEAN_VALUE | identifier | expression)
              | BOOLEAN_VALUE
              | identifier SQUARE_OPEN (identifier | integer_constant| expression)SQUARE_CLOSE
              | ROUND_OPEN (expression) ROUND_CLOSE

    assignment: identifier SQUARE_OPEN (integer_constant | identifier | expression) SQUARE_CLOSE ASSIGNMENT_OPERATOR expression
              | identifier (COMMA identifier)* ASSIGNMENT_OPERATOR (literal | identifier | expression) (COMMA (literal | identifier | expression))*
              | identifier index ASSIGNMENT_OPERATOR expression
              | identifier compound_operator expression

    index:     SQUARE_OPEN (expression | integer_constant) SQUARE_CLOSE 
              | index SQUARE_OPEN (expression |integer_constant) SQUARE_CLOSE
              
    control_flow: FUNCTION_DECLARATION identifier ROUND_OPEN parameters ROUND_CLOSE block
                | IF_ELIF ROUND_OPEN expression ROUND_CLOSE block
                | ELSE_KEYWORD block
                | WHILE_KEYWORD ROUND_OPEN expression ROUND_CLOSE block
                | DO_KEYWORD block WHILE_KEYWORD ROUND_OPEN expression ROUND_CLOSE
                | FOR_KEYWORD ROUND_OPEN dec_control_flow END_OF_STATEMENT expression END_OF_STATEMENT (expression | assignment) ROUND_CLOSE block
                | BREAK_CONTINUE END_OF_STATEMENT

    dec_control_flow: VARIABLE_DECLARATION identifier ASSIGNMENT_OPERATOR (literal | identifier | expression)

    declaration: TUPLE_DECLARATION identifier ASSIGNMENT_OPERATOR SQUARE_OPEN expression (COMMA expression)* SQUARE_CLOSE
                | LIST_DECLARATION identifier ASSIGNMENT_OPERATOR SQUARE_OPEN expression (COMMA expression)* SQUARE_CLOSE
                | LIST_DECLARATION identifier ASSIGNMENT_OPERATOR SQUARE_OPEN (COMMA | (expression))* SQUARE_CLOSE
                | ARR_DECLARATION identifier ASSIGNMENT_OPERATOR SQUARE_OPEN literal (COMMA literal)* SQUARE_CLOSE
                | EXCEPTION_TYPE identifier ASSIGNMENT_OPERATOR identifier
                | NULL_KEYWORD 
                | LIST_DECLARATION identifier ASSIGNMENT_OPERATOR matrix
                | ARR_DECLARATION  identifier ASSIGNMENT_OPERATOR matrix
                | VARIABLE_DECLARATION identifier (COMMA identifier)* ASSIGNMENT_OPERATOR (literal | identifier | expression) (COMMA (literal | identifier | expression))* 
    
    matrix : SQUARE_OPEN [items]SQUARE_CLOSE

    items: value (COMMA value)*
    value: matrix | literal

    exception_handling: TRY_KEYWORD block CATCH_KEYWORD ROUND_OPEN EXCEPTION_TYPE identifier ROUND_CLOSE block FINALLY_KEYWORD block
                       | THROW_KEYWORD EXCEPTION_TYPE ROUND_OPEN ROUND_CLOSE END_OF_STATEMENT


    block: CURLY_OPEN statements CURLY_CLOSE | CURLY_OPEN CURLY_CLOSE

    function_call: identifier ROUND_OPEN arguments ROUND_CLOSE
    | identifier DOT_OPERATOR identifier ROUND_OPEN arguments ROUND_CLOSE 


    operand: identifier
           | literal

    return_statement: RETURN_KEYWORD (expression)

    operator: OPERATOR

    compound_operator: COMPOUND_OPERATOR

    unary_operator: UNARY_OPERATOR

    comparator: COMPARATOR
    
    identifier: IDENTIFIER


    literal: integer_constant
           | decimal_constant
           | string_literal
           | BOOLEAN_VALUE

    keywords: KEYWORD

    integer_constant: INTEGER_CONSTANT

    decimal_constant: DECIMAL_CONSTANT

    string_literal: STRING_LITERAL

    arguments: (COMMA | expression)*

    parameters: parameter (COMMA parameter)*
                | (COMMA expression)*

    parameter: VARIABLE_DECLARATION identifier
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