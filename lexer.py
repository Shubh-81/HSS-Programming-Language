import re


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        keywords = ['var', 'const', 'if', 'elif', 'else', 'while', 'do', 'for', 'func', 'return', 'try', 'catch',
                    'finally', 'throw', 'print', 'true', 'false', 'tuple', 'list', 'arr']
        operators = ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '++', '--', '!', '=']
        parenthesis = ['(', ')', '{', '}', '[', ']']
        punctuation = [',', ':']
        endOfStatement = [';']

        source_code = re.sub(r'//.*', '', self.source_code)
        source_code = re.sub(r'\s+', ' ', source_code)


        # Updated regular expression to handle floating-point numbers, keywords, identifiers, and quotations
        tokens = re.findall(r'"(?:\\.|[^"])*"|\b\d+\.\d+\b|\b\d+\b|\b(?:' + '|'.join(
            map(re.escape, keywords)) + r')\b|\b[a-zA-Z_]\w*\b|[^\s\w]', source_code)
        print(tokens)

        for token in tokens:
            if re.match(r'^"[^"]*"$', token):
                self.tokens.append(('quotation', '\"'))
                self.tokens.append(('constant', token))  # Extract text without quotes
                self.tokens.append(('quotation', '\"'))
            elif token in keywords:
                self.tokens.append(('keyword', token))
            elif token in operators:
                self.tokens.append(('operator', token))
            elif token in punctuation:
                self.tokens.append(('punctuation', token))
            elif token in endOfStatement:
                self.tokens.append(('endOfStatement', token))
            elif token in parenthesis:
                self.tokens.append(('parenthesis', token))
            elif re.match(r'^\d+\.\d+$', token):
                self.tokens.append(('constant', token))  # Floating-point number
            elif re.match(r'^\d+$', token):
                self.tokens.append(('constant', token))
            elif re.match(r'^[a-zA-Z_]\w*$', token):
                self.tokens.append(('identifier', token))
            elif token == '"':
                self.tokens.append(('quotation', '\"'))
            else:
                self.tokens.append(('error', token))

    def get_tokens(self):
        return self.tokens


source_code = 'const pi = 3.14159; \nvar radius = 5; var area = pi * radius * radius; print("Area of circle =", area); radius++;'
lexer = Lexer(source_code)
lexer.tokenize()
tokens = lexer.get_tokens()
print(tokens)
