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
        keywords = ['var', 'const', 'if', 'elif', 'else', 'while', 'do', 'for', 'func', 'return', 'try', 'catch',
                    'finally', 'throw', 'print', 'true', 'false', 'tuple', 'list', 'arr', 'ExceptionType', 'null'
                    'break', 'continue', 'this', 'typeof']
        operators = ['+=', '-=', '++', '--', '+', '-', '*', '/', '%', '=']
        comparators = ['==', '!=', '<=', '>=', '<', '>', '!']
        parenthesis = ['(', ')', '{', '}', '[', ']']
        punctuation = [',', ':', '.']
        end_of_statement = [';']

        # Remove single-line comments (//) and compress consecutive whitespaces
        source_code = re.sub(r'//.*', '', self.source_code)
        source_code = re.sub(r'\s+', ' ', source_code)

        # Create regular expressions for operators and comparators
        operators_regex = '|'.join(map(re.escape, operators + comparators))
        continuous_operators_regex = rf'(?:{operators_regex})+'

        # Tokenize the source code using a regular expression to match different token types:
        # 1. Double-quoted strings, capturing escaped characters or any character except double quotes.
        # 2. Decimal numbers with optional integer part, decimal point, and fractional part.
        # 3. Integer numbers.
        # 4. Keywords (e.g., var, if) using a non-capturing group and word boundaries.
        # 5. Continuous sequences of operators (e.g., ++, +=).
        # 6. Identifiers (e.g., variable names) starting with a letter or underscore, followed by word characters.
        # 7. Any single character that is not a whitespace or word character, representing punctuation or special characters.

        tokens = re.findall(
            r'"(?:\\.|[^"])*"|\b\d+\.\d+\b|\b\d+\b|\b(?:' + '|'.join(map(re.escape, keywords)) + r')\b|' +
            continuous_operators_regex + r'|\b[a-zA-Z_]\w*\b|[^\s\w]',
            source_code)

        for token in tokens:
            if re.match(r'^"[^"]*"$', token):
                # Tokenize string literals: "example"
                self.tokens.append(('quotation', '\"'))
                self.tokens.append(('constant', token))
                self.tokens.append(('quotation', '\"'))
            elif token in keywords:
                # Tokenize keywords: var, if, else, etc.
                self.tokens.append(('keyword', token))
            elif token in operators:
                # Tokenize operators: +=, =, *, etc.
                self.tokens.append(('operator', token))
            elif token in comparators:
                # Tokenize comparators: ==, !=, <, etc.
                self.tokens.append(('comparator', token))
            elif token in punctuation:
                # Tokenize punctuation: ,, :, etc.
                self.tokens.append(('punctuation', token))
            elif token in end_of_statement:
                # Tokenize end of statement: ;
                self.tokens.append(('endOfStatement', token))
            elif token in parenthesis:
                # Tokenize parenthesis: (, ), {, }, [, ]
                self.tokens.append(('parenthesis', token))
            elif re.match(r'^\d+\.\d+$', token):
                # Tokenize decimal constants: 3.14
                self.tokens.append(('constant', token))
            elif re.match(r'^\d+$', token):
                # Tokenize integer constants: 123
                self.tokens.append(('constant', token))
            elif re.match(r'^[a-zA-Z_]\w*$', token):
                # Tokenize identifiers: variable names, function names, etc.
                self.tokens.append(('identifier', token))
            elif token == '"':
                # Tokenize standalone double quotes
                self.tokens.append(('quotation', '\"'))
            else:
                # Tokenize unrecognized tokens as errors
                self.tokens.append(('error', token))

    def get_tokens(self):
        return self.tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    lexer = Lexer(file_path=file_path)
    lexer.tokenize()
    tokens = lexer.get_tokens()
    print(tokens)
