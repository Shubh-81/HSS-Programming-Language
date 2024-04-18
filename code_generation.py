from parsing import parser
from parsing_ast import transformer
from semantic_analyzer import *
import parsing_ast

symbol_table = SymbolTable()
symbol_stack = {}
symbol_stack['global'] = symbol_table

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
        new_table = SymbolTable()
        symbol_stack[node.name.name] = new_table
        for idx, arg in enumerate(node.parameters.parameters):
            if arg.declaration_type.value == 'list':
                new_table.insert(ListSymbol(arg.identifier.name, type=new_table.lookup('INTEGER_CONSTANT'), category='parameter'))
            else:
                new_table.insert(VarSymbol(arg.identifier.name, type=new_table.lookup('INTEGER_CONSTANT'), category='parameter'))
        if not hasattr(node, '__dict__'):
            return symbol_table.lookup('NULL_VALUE')
        block_node = node.block
        children = [(k, v) for k, v in block_node.__dict__.items() if not k.startswith('_') and v]
        ou = None
        for idx, (attr, child) in enumerate(children):
            is_last = idx == len(children) - 1
            out = traverse_ast(child, last=is_last, symbol_table=new_table)
            if out and not ou:
                ou = out
            print(f'Out: {out}')
        return ou
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
        elif node.declaration_type.value == 'list':
            if not type(node.value) == parsing_ast.Matrix:
                raise Exception('Error: Expected a matrix')
            tp = None
            for idx, exp in enumerate(node.value.content.expressions):
                if tp == None:
                    tp = traverse_ast(exp, symbol_table)
                else:
                    if tp != traverse_ast(exp, symbol_table):
                        raise Exception('Error: Type mismatch in list')
            symbol_table.insert(ListSymbol(node.identifier.name, type=tp, category=node.declaration_type.value, length=len(node.value.content.expressions)))
        elif node.declaration_type.value == 'array':
            symbol_table.insert(VarSymbol(node.identifier.name, symbol_table.lookup('ARRAY'), node.declaration_type.value))
        else:
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
    ou = None
    for idx, (attr, child) in enumerate(children):
        is_last = idx == len(children) - 1
        out = traverse_ast(child, last=is_last, symbol_table=symbol_table)
        if out and not ou:
            ou = out
    return ou if ou else symbol_table.lookup('NULL_VALUE')

class CodeGenerator:
    def __init__(self):
        self.code = ["""
(module
(memory (export "memory") 1)
;; create a array
(func $arr (param $len i32) (result i32)
(local $offset i32)                              
(local.set $offset (i32.load (i32.const 0)))     

(i32.store (local.get $offset)                   
(local.get $len)
) 

(i32.store (i32.const 0)                        
(i32.add 
(i32.add
(local.get $offset)
(i32.mul 
(local.get $len) 
(i32.const 4)
)
)
(i32.const 4)                    
)
)
(local.get $offset)                             
)
;; return the array length
(func $len (param $arr i32) (result i32)
(i32.load (local.get $arr))
)
;; convert an element index to the offset of memory
(func $offset (param $arr i32) (param $i i32) (result i32)
(i32.add
(i32.add (local.get $arr) (i32.const 4))   
(i32.mul (i32.const 4) (local.get $i))     
)
)
;; set a value at the index 
(func $set (param $arr i32) (param $i i32) (param $value i32)
(i32.store 
(call $offset (local.get $arr) (local.get $i)) 
(local.get $value)
) 
)
;; get a value at the index 
(func $get (param $arr i32) (param $i i32) (result i32)
(i32.load 
(call $offset (local.get $arr) (local.get $i)) 
)
)
        """]
        self.variables = {}
        self.memory_offset = 0
        self.num_loops = 0

    def generate_code(self, node):
        method_name = 'generate_' + type(node).__name__
        method = getattr(self, method_name, self.default_generate)
        return method(node)

    def default_generate(self, node):
        raise Exception('No generate_{} method'.format(type(node).__name__))

    def generate_Statements(self, node):
        for child in node.statements:
            self.generate_code(child)

    def generate_VariableDeclaration(self, node):
        for identifier, value in zip(node.identifier, node.value):
            self.variables[identifier.name] = len(self.variables)
            self.generate_code(value)
            self.code.append('local.set ${}'.format(identifier.name))

    def generate_Declaration(self, node):
        self.variables[node.identifier.name] = self.memory_offset
        if type(node.declaration_type) == parsing_ast.DeclarationVariable and node.declaration_type.value == 'list':
            for i, value in enumerate(node.value.content.expressions):
                print(type(node.value.content.expressions))
                self.generate_code(value)
                self.code.append('local.set ${}'.format('temp'))
                self.code.append('(call $set (local.get ${}) (i32.const {}) (local.get ${}))'.format(node.identifier.name, i, 'temp'))
        else:
            self.generate_code(node.value)
            self.code.append('local.set ${}'.format(node.identifier.name))
        self.memory_offset += 4

    def generate_Function(self, node):
        self.variables = {}
        self.memory_offset = 0
        self.code.append('(func (export "{}")'.format(node.name))
        for param in node.parameters.parameters:
            name = param.identifier.name
            self.variables[name] = len(self.variables)
            self.code.append('(param ${} i32)'.format(name))
        self.code.append('(result i32)')
        self.code.append('(local $temp i32)')
        self.code.append('(local $temp2 i32)')
        for key, value in symbol_stack[node.name.name]._symbols.items():
            if type(value) == VarSymbol:
                if value.category != 'parameter':
                    if value.type.name == 'INTEGER_CONSTANT':
                        self.code.append('(local ${} i32)'.format(value.name))
                    elif value.type.name == 'DECIMAL_CONSTANT':
                        self.code.append('(local ${} f32)'.format(value.name))
                    elif value.type.name == 'BOOLEAN_VALUE':
                        self.code.append('(local ${} i32)'.format(value.name))
                    elif value.type.name == 'STRING_LITERAL':
                        self.code.append('(local ${} i32)'.format(value.name))
        for key, value in symbol_stack[node.name.name]._symbols.items():
            if type(value) == ListSymbol:
                if value.category != 'parameter':
                    if value.type.name == 'INTEGER_CONSTANT':
                        self.code.append('(local ${} i32)'.format(value.name))
                        self.code.append('(local.set ${} (call $arr (i32.const {})))'.format(value.name, value.length))
        self.generate_code(node.block)
        self.code.append('(i32.const 0)')
        self.code.append('return')
        self.code.append(')')

    def generate_FunctionCall(self, node):
        for arg in node.arguments.arguments:
            self.generate_code(arg)
        self.code.append('call ${}'.format(node.name))

    def generate_Return(self, node):
        self.generate_code(node.expression)
        self.code.append('return')

    def generate_Assignment(self, node):
        self.generate_code(node.identifier)
        self.generate_code(node.expression)
        self.code.append('local.set ${}'.format(node.identifier.name))

    def generate_IndexAssignment(self, node):
        self.generate_code(node.expression)
        self.code.append('local.set $temp2')
        self.generate_code(node.index)
        self.code.append('i32.const 1')
        self.code.append('i32.sub')
        self.code.append('local.set $temp')
        self.code.append('(call $set (local.get ${}) (local.get $temp) (local.get $temp2))'.format(node.identifier.name))

    def generate_Block(self, node):
        if node.statements:
            self.generate_code(node.statements)

    def generate_IfElse(self, node):
        self.generate_code(node.expression)
        self.code.append('if')
        self.generate_code(node.block)
        if node.else_block:
            self.code.append('else')
            self.generate_code(node.else_block)
        self.code.append('end')

    def generate_UnaryExpression(self, node):
        if type(node.children[0]) == parsing_ast.Index:
            self.generate_code(node.children[0])
            self.code.append('(i32.const 1)')
            self.code.append('i32.sub')
            self.code.append('local.set $temp')
            self.code.append('(call $get (local.get ${}) (local.get ${}))'.format(node.operator.name, 'temp'))
        elif type(node.operator) == parsing_ast.UnaryOperator:
            self.generate_code(node.children[0])
            if node.operator.operator == '--':
                self.code.append('i32.const 1')
                self.code.append('i32.sub')
                self.code.append('local.set ${}'.format(node.children[0].name))
            elif node.operator.operator == '++':
                self.code.append('i32.const 1')
                self.code.append('i32.add')
                self.code.append('local.set ${}'.format(node.children[0].name))
        elif type(node.children[0]) == parsing_ast.UnaryOperator:
            self.generate_code(node.operator)
            if node.children[0].operator == '--':
                self.code.append('i32.const 1')
                self.code.append('i32.sub')
                self.code.append('local.set ${}'.format(node.operator.name))
            elif node.children[0].operator == '++':
                self.code.append('i32.const 1')
                self.code.append('i32.add')
                self.code.append('local.set ${}'.format(node.operator.name))

    def generate_ForLoop(self, node):
        self.generate_code(node.dec_control_flow)
        self.num_loops += 1
        num_loops = self.num_loops
        self.code.append(f'(loop $forloop{num_loops} (block $breakforloop{num_loops}')
        self.generate_code(node.expression)
        self.code.append('i32.eqz')
        self.code.append(f'br_if $breakforloop{num_loops}')
        self.generate_code(node.block)
        self.generate_code(node.for_update)
        self.code.append(f'br $forloop{num_loops}')
        self.code.append('))')

    def generate_While(self, node):
        self.code.append('loop')
        self.generate_code(node.expression)
        self.code.append('if')
        self.generate_code(node.block)
        self.code.append('end')
        self.code.append('end')

    def generate_DoWhile(self, node):
        self.code.append('loop')
        self.generate_code(node.block)
        self.generate_code(node.expression)
        self.code.append('if')
        self.code.append('end')
        self.code.append('end')

    def generate_Matrix(self, node):
        for value in node.content.expressions:
            self.generate_code(value)
            self.code.append('local.set ${}'.format('temp'))

    def generate_Index(self, node):
        for expression in node.expressions:
            self.generate_code(expression)

    def generate_BinaryOp(self, node):
        self.generate_code(node.children[0])
        self.generate_code(node.children[1])
        if type(node.operator) == parsing_ast.Operator:
            if node.operator.operator == '+':
                self.code.append('i32.add')
            elif node.operator.operator == '-':
                self.code.append('i32.sub')
            elif node.operator.operator == '*':
                self.code.append('i32.mul')
            elif node.operator.operator == '/':
                self.code.append('i32.div_s')
            elif node.operator.operator == '%':
                self.code.append('i32.rem_s')
        elif type(node.operator) == parsing_ast.Comparator:
            if node.operator.comparator == '==':
                self.code.append('i32.eq')
            elif node.operator.comparator == '!=':
                self.code.append('i32.ne')
            elif node.operator.comparator == '<':
                self.code.append('i32.lt_s')
            elif node.operator.comparator == '<=':
                self.code.append('i32.le_s')
            elif node.operator.comparator == '>':
                self.code.append('i32.gt_s')
            elif node.operator.comparator == '>=':
                self.code.append('i32.ge_s')
        elif type(node.operator) == parsing_ast.CompoundOperator:
            if node.operator.operator == '+=':
                self.code.append('i32.add')
            elif node.operator.operator == '-=':
                self.code.append('i32.sub')
            elif node.operator.operator == '*=':
                self.code.append('i32.mul')
            elif node.operator.operator == '/=':
                self.code.append('i32.div_s')
            elif node.operator.operator == '%=':
                self.code.append('i32.rem_s')
            self.code.append('local.set ${}'.format(node.children[0].name))

    def generate_Literal(self, node):
        if node.type == 'INTEGER_CONSTANT':
            self.code.append('i32.const {}'.format(node.value))
        elif node.type == 'DECIMAL_CONSTANT':
            self.code.append('f32.const {}'.format(node.value))
        elif node.type == 'BOOLEAN_VALUE':
            self.code.append('i32.const {}'.format(node.value))

    def generate_Identifier(self, node):
        self.code.append('local.get ${}'.format(node.name))

    def get_code(self):
        return '\n'.join(self.code)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python code_generation.py <path_to_hss_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        data = file.read()
    tree = parser.parse(data)
    ast = transformer.transform(tree)
    traverse_ast(ast, symbol_table)
    code_generator = CodeGenerator()
    code_generator.generate_code(ast)
    code = code_generator.get_code()
    code += '\n)'
    with open('out.wat', 'w') as file:
        file.write(code)
    print('Code generation successful')
    print(f'Wat code written to out.wat')
