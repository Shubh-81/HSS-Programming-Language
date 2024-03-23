import re
import sys


class Lexer:
    def __init__(self, source_code=None, file_path=None):
        if source_code is not None:
            self.source_code = source_code
        elif file_path is not None:
            with open(file_path, 'r') as file:
                self.source_code = file.read()
        else:
            raise ValueError("Either 'source_code' or 'file_path' must be provided.")

        self.tokens = []

    def tokenize(self):
        # Define language elements: keywords, operators, comparators, etc.
        keywords = ['this', 'typeof']
        operators = ["+", "-", "*", "/", "%", "&", "|"]
        boolean_values = ["true", "false"]
        compound_operators = ["+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "|=", "^="]
        unary_operators = ["++", "--"]
        comparators = ['==', '!=', '<=', '>=', '<', '>', '||', '&&']
        punctuation = [':']
        dot_operator = ['.']
        end_of_statement = [';']
        print_keyword = ['print']
        comma = [',']
        round_open = ['(']
        round_close = [')']
        curly_open = ['{']
        curly_close = ['}']
        square_open = ['[']
        square_close = [']']
        return_keyword = ['return']
        variable_declaration = ['var', 'const']
        not_operator = ['!']
        assignment_operator = ['=']
        function_declaration = ['func']
        if_elif = ['if', 'elif']
        else_keyword = ['else']
        while_keyword = ['while']
        do_keyword = ['do']
        for_keyword = ['for']
        tuple_declaration = ['tuple']
        list_declaration = ['list']
        arr_declaration = ['arr']
        # For break and continue
        break_continue = ['break', 'continue']
        exception_keyword = ['ExceptionType']
        null_keyword = ['null']
        try_keyword = ['try']
        catch_keyword = ['catch']
        finally_keyword = ['finally']
        throw_keyword = ['throw']
        # Remove multi-line comments (/* */) and compress consecutive whitespaces
        source_code = re.sub(r'/\*.*?\*/', '', self.source_code, flags=re.DOTALL)
        source_code = re.sub(r'\s+', ' ', source_code)

        # Create regular expressions for operators and comparators
        # Create regular expressions for operators and comparators
        operators_regex = '|'.join(map(re.escape, operators + comparators))
        # Include compound operators in the regex but prioritize them before shorter operators
        continuous_operators_regex = rf'(?:{"|".join(map(re.escape, compound_operators))}|{operators_regex})+'


        # Tokenize the source code using a regular expression to match different token types
        tokens = re.findall(
            r'"(?:\\.|[^"])*"|\b\d+\.\d+\b|\b\d+\b|\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b|' +
            r'\b(?:[a-zA-Z_]\w*|[0-9]+[a-zA-Z_]\w*)\b|' + continuous_operators_regex + r'|\b[a-zA-Z_]\w*\b|[^\s\w]',
            source_code)
        print(tokens)
        for token in tokens:
            if re.match(r'^"[^"]*"$', token):
                # Tokenize string literals: "example"
                self.tokens.append(('STRING_LITERAL', token))
            elif token in boolean_values:
                # Tokenize boolean values: true, false
                self.tokens.append(('BOOLEAN_VALUE', token))
            elif token in comma:
                # Tokenize comma
                self.tokens.append(('COMMA', token))
            elif token in function_declaration:
                # Tokenize function declaration
                self.tokens.append(('FUNCTION_DECLARATION', token))
            elif token in break_continue:
                # Tokenize break and continue
                self.tokens.append(('BREAK_CONTINUE', token))
            elif token in if_elif:
                # Tokenize if and elif
                self.tokens.append(('IF_ELIF', token))
            elif token in else_keyword:
                # Tokenize else keyword
                self.tokens.append(('ELSE_KEYWORD', token))
            elif token in while_keyword:
                # Tokenize while keyword
                self.tokens.append(('WHILE_KEYWORD', token))
            elif token in do_keyword:
                # Tokenize do keyword
                self.tokens.append(('DO_KEYWORD', token))
            elif token in for_keyword:
                # Tokenize for keyword
                self.tokens.append(('FOR_KEYWORD', token))
            elif token in print_keyword:
                # Tokenize print keyword
                self.tokens.append(('PRINT_KEYWORD', token))
            elif token in return_keyword:
                # Tokenize return keyword
                self.tokens.append(('RETURN_KEYWORD', token))
            elif token in variable_declaration:
                # Tokenize variable declaration: var, const
                self.tokens.append(('VARIABLE_DECLARATION', token))
            elif token in list_declaration:
                # Tokenize list declaration: list
                self.tokens.append(('LIST_DECLARATION', token))
            elif token in arr_declaration:
                # Tokenize arr declaration: arr
                self.tokens.append(('ARR_DECLARATION', token))
            elif token in tuple_declaration:
                # Tokenize tuple declaration: tuple
                self.tokens.append(('TUPLE_DECLARATION', token))
            elif token in exception_keyword:
                # Tokenize exception type
                self.tokens.append(('EXCEPTION_TYPE', token))
            elif token in null_keyword:
                # Tokenize null keyword
                self.tokens.append(('NULL_KEYWORD', token))
            elif token in try_keyword:
                # Tokenize try keyword
                self.tokens.append(('TRY_KEYWORD', token))
            elif token in catch_keyword:
                # Tokenize catch keyword
                self.tokens.append(('CATCH_KEYWORD', token))
            elif token in finally_keyword:
                # Tokenize finally keyword
                self.tokens.append(('FINALLY_KEYWORD', token))
            elif token in throw_keyword:
                # Tokenize throw keyword
                self.tokens.append(('THROW_KEYWORD', token))
            elif token in keywords:
                # Tokenize keywords: var, if, else, etc.
                self.tokens.append(('KEYWORD', token))
            elif token in not_operator:
                # Tokenize not operator: !
                self.tokens.append(('NOT_OPERATOR', token))
            elif token in operators:
                # Tokenize operators: +=, =, *, etc.
                self.tokens.append(('OPERATOR', token))
            elif token in compound_operators:
                # Tokenize compound operators: +=, -=, *=, etc.
                self.tokens.append(('COMPOUND_OPERATOR', token))
            elif token in unary_operators:
                # Tokenize unary operators: ++, --
                self.tokens.append(('UNARY_OPERATOR', token))
            elif token in comparators:
                # Tokenize comparators: ==, !=, <, etc.
                self.tokens.append(('COMPARATOR', token))
            elif token in dot_operator:
                # Tokenize dot operator: .
                self.tokens.append(('DOT_OPERATOR', token))
            elif token in punctuation:
                # Tokenize punctuation: ,, :, etc.
                self.tokens.append(('PUNCTUATION', token))
            elif token in assignment_operator:
                # Tokenize assignment operator: =
                self.tokens.append(('ASSIGNMENT_OPERATOR', token))
            elif token in end_of_statement:
                # Tokenize end of statement: ;
                self.tokens.append(('END_OF_STATEMENT', token))
            elif token in round_open:
                # Tokenize round open: (
                self.tokens.append(('ROUND_OPEN', token))
            elif token in round_close:
                # Tokenize round close: )
                self.tokens.append(('ROUND_CLOSE', token))
            elif token in curly_open:
                # Tokenize curly open: {
                self.tokens.append(('CURLY_OPEN', token))
            elif token in curly_close:
                # Tokenize curly close: }
                self.tokens.append(('CURLY_CLOSE', token))
            elif token in square_open:
                # Tokenize square open: [
                self.tokens.append(('SQUARE_OPEN', token))
            elif token in square_close:
                # Tokenize square close: ]
                self.tokens.append(('SQUARE_CLOSE', token))
            elif re.match(r'^\d+\.\d+$', token):
                # Tokenize decimal constants: 3.14
                self.tokens.append(('DECIMAL_CONSTANT', token))
            elif re.match(r'^\d+$', token):
                # Tokenize integer constants: 123
                self.tokens.append(('INTEGER_CONSTANT', token))
            elif re.match(r'^[a-zA-Z_]\w*$', token):
                # Tokenize identifiers: variable names, function names, etc.
                self.tokens.append(('IDENTIFIER', token))
            elif token == '"':
                # Tokenize standalone double quotes
                self.tokens.append(('QUOTATION', '\"'))
            else:
                # Tokenize unrecognized tokens as errors
                self.tokens.append(('ERROR', token))

    def get_tokens(self):
        return self.tokens


def print_tokens(tokens):
    for token_type, token_value in tokens:
        print(f'{token_type}: {token_value}')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    lexer = Lexer(file_path=file_path)
    lexer.tokenize()
    tokens = lexer.get_tokens()
    print_tokens(tokens)
