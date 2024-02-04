import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        keywords = ['var', 'const', 'if', 'elif', 'else', 'while', 'do', 'for', 'func', 'return', 'try', 'catch',
                    'finally',
                    'throw', 'print', 'true', 'false', 'tuple', 'list', 'arr']
        unary_operators=['==','!=','<=','>=','+=','-=','++','--']
        operators=['+','-','*','/','!','=','%','>','<']
        parenthesis = ['(', ')', '{', '}', '[', ']']
        punctuation = [',', ':', '"', "'",'.']
        endOfStatement = [';']

        source_code = re.sub(r'//.*', '', self.source_code) # removes all comments
        source_code = re.sub(r'\s+', ' ', source_code) # removes multiple white spaces

        tokens = re.findall(r'".*?"|\w+|\d+|[^\s\w]', source_code)

        i = 0
        while i < len(tokens)-1:
            a = tokens[i] + tokens[i+1]
            if a in unary_operators:
                self.tokens.append(('uninary_operator', a))
                tokens = tokens[:i] + tokens[i+2:]
            else:
                 i += 1 

        for token in tokens:
            if re.match(r'^"[^"]*"$', token): 
                self.tokens.append(('constant', token))
            elif token in keywords:
                self.tokens.append(('keyword', token))
            elif token in operators:
                self.tokens.append(('operator', token))
            elif token in punctuation:
                self.tokens.append(('punctuation', token))
            elif token in punctuation:
                self.tokens.append(('punctuation', token))
            elif token in endOfStatement:
                self.tokens.append(('endOfStatement', token))
            elif token in parenthesis:
                self.tokens.append(('parenthesis', token))
            elif re.match(r'^[0-9]+$', token): # this expression takes care of all the numbers
                self.tokens.append(('constant', token))
            elif re.match(r'^[a-zA-Z_]\w*$', token): # this takes care of all kinds of variable names
                self.tokens.append(('identifier', token))
            else:
                self.tokens.append(('error', token))

    def get_tokens(self):
        return self.tokens


file_path='your_file_location'
try:
    with open(file_path, 'r') as file:
        source_code = file.read()
        print(source_code)
except FileNotFoundError:
    print(f"File not found: '{file_path}'")
except Exception as e:
    print(f"An error occurred: {e}")


lexer = Lexer(source_code)
lexer.tokenize()
tokens = lexer.get_tokens()
print(tokens)
