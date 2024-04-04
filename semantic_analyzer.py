from parsing import parser
from parsing_ast import transformer
import parsing_ast
import sys

class Symbol(object):
    def __init__(self, name, type=None, category=None) -> None:
        self.name = name
        self.type = type
        self.category = category

    def __str__(self) -> str:
        return f'{self.name} {self.type} {self.category}'
    
    def __repr__(self) -> str:
        return self.__str__()

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )

class VarSymbol(Symbol):
    def __init__(self, name, type=None, category=None) -> None:
        super().__init__(name, type, category)
    
    def __str__(self) -> str:
        return "<{class_name}(name='{name}', type='{type}', category='{category}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
            category=self.category
        )
    
    __repr__ = __str__

class ListSymbol(Symbol):
    def __init__(self, name, type=None, category=None) -> None:
        super().__init__(name, type, category)
    
    def __str__(self) -> str:
        return "<{class_name}(name='{name}', type='{type}', category='{category}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
            category=self.category
        )
    
    __repr__ = __str__

class SymbolTable(object):
    def __init__(self) -> None:
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self) -> None:
        self.insert(BuiltinTypeSymbol('INTEGER_CONSTANT'))
        self.insert(BuiltinTypeSymbol('DECIMAL_CONSTANT'))
        self.insert(BuiltinTypeSymbol('STRING_LITERAL'))
        self.insert(BuiltinTypeSymbol('BOOLEAN_VALUE'))
        self.insert(BuiltinTypeSymbol('NULL_VALUE'))
        self.insert(BuiltinTypeSymbol('ARRAY'))
        self.insert(BuiltinTypeSymbol('TUPLE'))
        self.insert(BuiltinTypeSymbol('LIST'))

    def __str__(self) -> str:
        symtab_header = 'Symbol table contents'
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__

    def insert(self, symbol) -> None:
        print('Insert: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name) -> Symbol:
        print('Lookup: %s' % name)
        return self._symbols.get(name, None)

symbol_table = SymbolTable()
symbol_stack = [symbol_table]

def traverse_ast(node, symbol_table, last=True):
    node_type = type(node) 
    print(node_type)
    if isinstance(node, list):
        for idx, item in enumerate(node):
            if idx == len(node) - 1:
                out = traverse_ast(item, last=True, symbol_table=symbol_table)
            else:
                out = traverse_ast(item, last=False, symbol_table=symbol_table)
        return out
    if type(node) == parsing_ast.Return:
        res = traverse_ast(node.expression, symbol_table)
        return res
    if isinstance(node, parsing_ast.BinaryOp):
        left_type = traverse_ast(node.children[0], symbol_table)
        right_type = traverse_ast(node.children[1], symbol_table)
        if isinstance(node.operator, parsing_ast.Operator) or isinstance(node.operator, parsing_ast.CompoundOperator):
            if node.operator.operator in ['+','+=']:
                print(left_type.name, right_type.name)
                if left_type.name == 'STRING_LITERAL' and right_type.name == 'STRING_LITERAL':
                    return symbol_table.lookup('STRING_LITERAL')
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('INTEGER_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                raise Exception('Type mismatch')
            elif node.operator.operator in ['-', '*', '-=', '*=']:
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('INTEGER_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                raise Exception('Type mismatch')
            elif node.operator.operator in ['/','%','/=', '%=']:
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                raise Exception('Type mismatch')
            elif node.operator.operator in ['&', '|']:
                if left_type.name == 'BOOLEAN_VALUE' and right_type.name == 'BOOLEAN_VALUE':
                    return symbol_table.lookup('BOOLEAN_VALUE')
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('INTEGER_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'INTEGER_CONSTANT' and right_type.name == 'DECIMAL_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                if left_type.name == 'DECIMAL_CONSTANT' and right_type.name == 'INTEGER_CONSTANT':
                    return symbol_table.lookup('DECIMAL_CONSTANT')
                raise Exception('Type mismatch')
            elif node.operator.operator in ["<<=", ">>=", "&=", "|=", "^="]:
                if left_type.name == right_type.name:
                    return symbol_table.lookup('BOOLEAN_VALUE')
                raise Exception('Type mismatch')
        elif isinstance(node.operator, parsing_ast.Comparator) and node.operator.comparator in ['==', '!=', '<=', '>=', '<', '>', '||', '&&']:
            if left_type.name == right_type.name:
                return symbol_table.lookup('BOOLEAN_VALUE')
            raise Exception('Type mismatch')
        elif isinstance(node.operator, parsing_ast.CompoundOperator):
            symbol = symbol_table.lookup(node.children[0].name)
            symbol.type = traverse_ast(node, symbol_table)
        else:
            raise Exception('Unknown operator') 
    if type(node) == parsing_ast.Function:
        if symbol_table.lookup(node.name.name):
            raise Exception('Error: Duplicate Function Declaration: %s' % node.name.name)
        symbol_table.insert(VarSymbol(node.name.name, type=node, category='function'))
        return
    if isinstance(node, parsing_ast.InbuiltFunctionCall):
        if not symbol_table.lookup(node.base.name):
            raise Exception('Error: Symbol not found: %s' % node.base.name)
    if type(node) == parsing_ast.FunctionCall:
        if not symbol_table.lookup(node.name.name):
            raise Exception('Error: Symbol not found: %s' % node.name.name)
        if not isinstance(symbol_table.lookup(node.name.name).type, parsing_ast.Function):
            raise Exception('Error: %s is not a function' % node.name.name)
        if len(node.arguments.arguments) != len(symbol_table.lookup(node.name.name).type.parameters.parameters):
            raise Exception('Error: Mismatch in number of arguments')
        new_table = SymbolTable()
        symbol_stack.append(new_table)
        for idx, arg in enumerate(node.arguments.arguments):
            nnode = symbol_table.lookup(node.name.name).type.parameters.parameters[idx]
            if isinstance(arg, parsing_ast.Identifier):
                if not symbol_table.lookup(arg.name):
                    raise Exception('Error: Symbol not found: %s' % arg.name)
                new_table.insert(VarSymbol(nnode.identifier.name, symbol_table.lookup(arg.name).type, nnode.declaration_type.value))
            if isinstance(arg, parsing_ast.Literal):
                new_table.insert(VarSymbol(nnode.identifier.name, symbol_table.lookup(arg.type), nnode.declaration_type.value))
        if not hasattr(node, '__dict__'):
            return symbol_table.lookup('NULL_VALUE')
        node = symbol_table.lookup(node.name.name).type.block
        children = [(k, v) for k, v in node.__dict__.items() if not k.startswith('_') and v]
        for idx, (attr, child) in enumerate(children):
            is_last = idx == len(children) - 1
            out = traverse_ast(child, last=is_last, symbol_table=new_table)
            print(f'Out: {out}')
        return out
    if isinstance(node, parsing_ast.VariableDeclaration):
        if len(node.identifier) != len(node.value):
            raise Exception('Error: Mismatch in number of identifiers and values')
        for idx, identifier in enumerate(node.identifier):
            if symbol_table.lookup(identifier.name):
                raise Exception('Error: Duplicate identifier found: %s' % identifier.name)
            if isinstance(node.value[idx], parsing_ast.Identifier) and not symbol_table.lookup(node.value[idx].name):
                raise Exception('Error: Symbol not found: %s' % node.value[idx].name)
            symbol_table.insert(VarSymbol(identifier.name, traverse_ast(node.value[idx], symbol_table), node.declaration_type.value))

    if isinstance(node, parsing_ast.Declaration):
        if symbol_table.lookup(node.identifier.name):
            raise Exception('Error: Duplicate identifier found: %s' % node.identifier.name)
        if node.declaration_type.value == 'tuple':
            symbol_table.insert(VarSymbol(node.identifier.name, symbol_table.lookup('TUPLE'), node.declaration_type.value))
        if node.declaration_type.value == 'list':
            if not type(node.value) == parsing_ast.Matrix:
                raise Exception('Error: Expected a matrix')
            tp = None
            for idx, exp in enumerate(node.value.content.expressions):
                if tp == None:
                    tp = traverse_ast(exp, symbol_table)
                else:
                    if tp != traverse_ast(exp, symbol_table):
                        raise Exception('Error: Type mismatch in list')
            symbol_table.insert(VarSymbol(node.identifier.name, type=tp, category=node.declaration_type.value))
        if node.declaration_type.value == 'array':
            symbol_table.insert(VarSymbol(node.identifier.name, symbol_table.lookup('ARRAY'), node.declaration_type.value))
        if isinstance(node.value, parsing_ast.Identifier) and not symbol_table.lookup(node.value.name):
            raise Exception('Error: Symbol not found: %s' % node.value.name)
        symbol_table.insert(VarSymbol(node.identifier.name, traverse_ast(node.value, symbol_table), node.declaration_type.value))
    if isinstance(node, parsing_ast.Assignment):
        if not symbol_table.lookup(node.identifier.name):
            raise Exception('Error: Symbol not found: %s' % node.identifier.name)
        if symbol_table.lookup(node.identifier.name).category == 'const':
            raise Exception('Error: Cannot assign to constant: %s' % node.identifier.name)
        if isinstance(node.expression, parsing_ast.Identifier) and not symbol_table.lookup(node.expression.name):
            raise Exception('Error: Symbol not found: %s' % node.expression.name)
        symbol = symbol_table.lookup(node.identifier.name)
        symbol.type = traverse_ast(node.expression, symbol_table)
    if type(node) == parsing_ast.FunctionArgumentList:
        for arg in node.arguments:
            if isinstance(arg, parsing_ast.Identifier) and not symbol_table.lookup(arg.name):
                raise Exception('Error: Symbol not found: %s' % arg.name)
    if type(node) == parsing_ast.PrintArgumentList:
        for arg in node.arguments:
            if isinstance(arg, parsing_ast.Identifier) and not symbol_table.lookup(arg.name):
                raise Exception('Error: Symbol not found: %s' % arg.name)
    if type(node) == parsing_ast.IfElse:
        if isinstance(node.expression, parsing_ast.Identifier) and not symbol_table.lookup(node.expression.name):
            raise Exception('Error: Symbol not found: %s' % node.expression.name)
    if type(node) == parsing_ast.While:
        if isinstance(node.expression, parsing_ast.Identifier) and not symbol_table.lookup(node.expression.name):
            raise Exception('Error: Symbol not found: %s' % node.expression.name)
    if type(node) == parsing_ast.DoWhile:
        if isinstance(node.expression, parsing_ast.Identifier) and not symbol_table.lookup(node.expression.name):
            raise Exception('Error: Symbol not found: %s' % node.expression.name)
    if type(node) == parsing_ast.BinaryOp:
        if isinstance(node.children[0], parsing_ast.Identifier) and not symbol_table.lookup(node.children[0].name):
            raise Exception('Error: Symbol not found: %s' % node.children[0].name)
        if isinstance(node.children[1], parsing_ast.Identifier) and not symbol_table.lookup(node.children[1].name):
            raise Exception('Error: Symbol not found: %s' % node.children[1].name)
    if type(node) == parsing_ast.UnaryExpression:
        if isinstance(node.children[0], parsing_ast.Identifier) and not symbol_table.lookup(node.children[0].name):
            raise Exception('Error: Symbol not found: %s' % node.children[0].name)
        if isinstance(node.operator, parsing_ast.Identifier) and not symbol_table.lookup(node.operator.name):
            raise Exception('Error: Symbol not found: %s' % node.operator.name)
    if isinstance(node, parsing_ast.Literal):
        return symbol_table.lookup(node.type)
    if isinstance(node, parsing_ast.Identifier):
        if not symbol_table.lookup(node.name):
            raise Exception('Error: Symbol not found: %s' %node.name)
        symbol = symbol_table.lookup(node.name)
        return symbol_table.lookup(node.name).type
    if not hasattr(node, '__dict__'):
        return symbol_table.lookup('NULL_VALUE')
    children = [(k, v) for k, v in node.__dict__.items() if not k.startswith('_') and v]
    for idx, (attr, child) in enumerate(children):
        is_last = idx == len(children) - 1
        out = traverse_ast(child, last=is_last, symbol_table=symbol_table)
        if out:
            return out
    return symbol_table.lookup('NULL_VALUE')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python semantic_analyzer.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        source_code = file.read()
    try:
        tree = parser.parse(source_code)
        ast = transformer.transform(tree)
        traverse_ast(ast, symbol_table)
        print("Semantic analysis successful.")
        for symbol in symbol_stack:
            print(symbol)
    except Exception as e:
        print("Semantic analysis failed:", e)
        sys.exit(1)
    