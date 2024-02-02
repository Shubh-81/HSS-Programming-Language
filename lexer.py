import re


class Token:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return f'<{self.name}, "{self.value}">'


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        keywords = ['var', 'const', 'if', 'elif', 'else', 'while', 'do', 'for', 'func', 'return', 'try', 'catch',
                    'finally',
                    'throw', 'print', 'true', 'false', 'tuple', 'list', 'arr']
        operators = ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '++', '--', '!', '=']
        parenthesis = ['(', ')', '{', '}', '[', ']']
        punctuation = [',', ':', '"', "'"]
        endOfStatement = [';']

        source_code = re.sub(r'//.*', '', self.source_code)
        source_code = re.sub(r'\s+', ' ', source_code)

        tokens = re.findall(r'".*?"|\w+|\d+|[^\s\w]', source_code)
        for token in tokens:
            if re.match(r'^"[^"]*"$', token):
                self.tokens.append(('constant', token))
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
            elif re.match(r'^[0-9]+$', token):
                self.tokens.append(('constant', token))
            elif re.match(r'^[a-zA-Z_]\w*$', token):
                self.tokens.append(('identifier', token))
            else:
                self.tokens.append(('error', token))

    def get_tokens(self):
        return self.tokens


source_code = 'const pi = 3.14159; var radius = 5; var area = pi * radius * radius; print("Area of circle =", area);'
lexer = Lexer(source_code)
lexer.tokenize()
tokens = lexer.get_tokens()
print(tokens)
