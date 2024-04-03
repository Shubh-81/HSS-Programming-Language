from lark import Lark, Tree
from lexer import Lexer as Lexer_
import logging
from typing import List
from dataclasses import dataclass
import lark
from parsing import parser
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class ASTNode:
    """Abstract base class for abstract sequence of sequence of sums"""
    def __init__(self):
        """This is an abstract class and should not be instantiated"""
        this_class = self.__class__.__name__
        if this_class == "ASTNode":
            raise NotImplementedError("ASTNode is an abstract class and should not be instantiated")
        else:
            raise NotImplementedError(f"{this_class} is missing a constructor method")
        
class Statement(ASTNode):
    pass

class Statements(ASTNode):
    def __init__(self):
        self.statements: List[Statement] = []
    
    def append(self, statement: Statement):
        self.statements.append(statement)

    def __str__(self) -> str:
        el_strs = ", ".join(str(e) for e in self.statements)
        return f"[{el_strs}]"

    def __repr__(self):
        return f"statements({repr(self.statements)})"
    
class VariableDeclaration(ASTNode):
    def __init__(self, declaration_type, identifier, value):
        self.declaration_type = declaration_type
        self.identifier = identifier
        self.value = value

    def __str__(self) -> str:
        identifiers = ", ".join(str(e) for e in self.identifier)
        values = ", ".join(str(e) for e in self.value)
        return f"{self.declaration_type} {identifiers} = {values}"
    
    def __repr__(self):
        return f"declaration({repr(self.declaration_type)}, {repr(self.identifier)}, {repr(self.value)})"

class Declaration(ASTNode):
    def __init__(self, declaration_type, identifier, value):
        self.declaration_type = declaration_type
        self.identifier = identifier
        self.value = value

    def __str__(self) -> str:
        return f"{self.declaration_type} {self.identifier} = {self.value}"
    
    def __repr__(self):
        return f"declaration({repr(self.declaration_type)}, {repr(self.identifier)}, {repr(self.value)})"
    
class DeclarationVariable(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"
    
    def __repr__(self):
        return f"declaration_variable({repr(self.value)})"

class ExceptionDeclaration(ASTNode):
    def __init__(self, exception_type, identifier, value):
        self.exception_type = exception_type
        self.identifier = identifier
        self.value = value

    def __str__(self) -> str:
        return f"{self.exception_type} {self.identifier} = {self.value}"
    
    def __repr__(self):
        return f"exception_declaration({repr(self.exception_type)}, {repr(self.identifier)}, {repr(self.value)})"

class Matrix(ASTNode):
    def __init__(self, content):
        self.content = content

    def __str__(self) -> str:
        return str(self.content)
    
    def __repr__(self):
        return f"matrix({repr(self.content)})"

class MatrixList(ASTNode):
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __str__(self) -> str:
        itmes = ", ".join(str(e) for e in self.items)
        return f"[{itmes}]"
    
    def __repr__(self):
        return f"matrix_list({repr(self.items)})"

class MatrixExpressionList(ASTNode):
    def __init__(self):
        self.expressions = []

    def add_expression(self, expression):
        self.expressions.append(expression)

    def __str__(self) -> str:
        expr = ", ".join(str(e) for e in self.expressions)
        return f"[{expr}]"
    
    def __repr__(self):
        return f"matrix_expression_list({repr(self.expressions)})"

@dataclass
class ExceptionHandling(Statement):
    pass

class TryCatchFinally(ExceptionHandling):
    def __init__(self, try_block, exception_type, identifier, catch_block, finally_block):
        self.try_block = try_block
        self.exception_type = exception_type
        self.identifier = identifier
        self.catch_block = catch_block
        self.finally_block = finally_block

    def __str__(self) -> str:
        return f"try {self.try_block} catch ({self.exception_type} {self.identifier}) {self.catch_block} finally {self.finally_block}"
    
    def __repr__(self):
        return f"try_catch_finally({repr(self.try_block)}, {repr(self.exception_type)}, {repr(self.identifier)}, {repr(self.catch_block)}, {repr(self.finally_block)})"

class Throw(ExceptionHandling):
    def __init__(self, exception_type, arguments):
        self.exception_type = exception_type
        self.arguments = arguments

    def __str__(self) -> str:
        return f"throw {self.exception_type}({self.arguments})"
    
    def __repr__(self):
        return f"throw({repr(self.exception_type)}, {repr(self.arguments)})"
    
class Block(ASTNode):
    def __init__(self, statements=None):
        self.statements = statements

    def __str__(self) -> str:
        return f"{self.statements}" if self.statements else "{}"
    
    def __repr__(self):
        return f"block({repr(self.statements)})"

class Return(Statement):
    def __init__(self, expression = None):
        self.expression = expression

    def __str__(self) -> str:
        return f"return {self.expression}" if self.expression else "return"
    
    def __repr__(self):
        return f"return({repr(self.expression)})" if self.expression else "return()"

@dataclass
class Control(Statement):
    pass

class Function(Control):
    def __init__(self, name, parameters, block):
        self.name = name
        self.parameters = parameters
        self.block = block

    def __str__(self) -> str:
        return f"function {self.name}({self.parameters}) {self.block}"
    
    def __repr__(self):
        return f"function({repr(self.name)}, {repr(self.parameters)}, {repr(self.block)})"
    
class Parameters(Function):
    def __init__(self):
        self.parameters = []

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def __str__(self) -> str:
        return f"{self.parameters}"
    
    def __repr__(self):
        return f"parameters({repr(self.parameters)})"
    
class Parameter(Parameters):
    def __init__(self, declaration_type, identifier):
        self.declaration_type = declaration_type
        self.identifier = identifier

    def __str__(self) -> str:
        return f"{self.declaration_type} {self.identifier}"
    
    def __repr__(self):
        return f"parameter({repr(self.declaration_type)}, {repr(self.identifier)})"

class IfElse(Control):
    def __init__(self, expression, block, else_block):
        self.expression = expression
        self.block = block
        self.else_block = else_block

    def __str__(self) -> str:
        return f"if-elif ({self.expression}) {self.block} else {self.else_block}"
    
    def __repr__(self):
        return f"if_else({repr(self.expression)}, {repr(self.block)}, {repr(self.else_block)})"

class While(Control):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block

    def __str__(self) -> str:
        return f"while ({self.expression}) {self.block}"
    
    def __repr__(self):
        return f"while({repr(self.expression)}, {repr(self.block)})"

class DoWhile(Control):
    def __init__(self, block, expression):
        self.block = block
        self.expression = expression

    def __str__(self) -> str:
        return f"do {self.block} while ({self.expression})"
    
    def __repr__(self):
        return f"do_while({repr(self.block)}, {repr(self.expression)})"

class ForLoop(Control):
    def __init__(self, dec_control_flow, expression, for_update, block):
        self.dec_control_flow = dec_control_flow
        self.expression = expression
        self.for_update = for_update
        self.block = block

    def __str__(self) -> str:
        return f"for ({self.dec_control_flow}; {self.expression}; {self.for_update}) {self.block}"
    
    def __repr__(self):
        return f"for_loop({repr(self.dec_control_flow)}, {repr(self.expression)}, {repr(self.for_update)}, {repr(self.block)})"

class BreakContinue(Control):
    def __init__(self, keyword):
        self.keyword = keyword

    def __str__(self) -> str:
        return f"{self.keyword}"
    
    def __repr__(self):
        return f"break_continue({repr(self.keyword)})"

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

class Expression(ASTNode):
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class Assignment(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __str__(self) -> str:
        return f"{self.identifier} = {self.expression}"
    
    def __repr__(self):
        return f"assignment({repr(self.identifier)}, {repr(self.expression)})"

class BinaryOp(Expression):
    def __init__(self, operator, left: Expression, right: Expression):
        super().__init__()
        self.operator = operator
        self.add_child(left)
        self.add_child(right)

    def __str__(self) -> str:
        return f"{self.children[0]} {self.operator} {self.children[1]}"
    
    def __repr__(self):
        return f"binary_op({repr(self.operator)}, {repr(self.children[0])}, {repr(self.children[1])})"
    
class BinaryDotOp(Expression):
    def __init__(self, base, name, expression):
        super().__init__()
        self.base = base
        self.name = name
        self.add_child(expression)

    def __str__(self) -> str:
        return f"{self.base}.{self.name}({self.children[0]})"
    
    def __repr__(self):
        return f"binary_dot_op({repr(self.base)}, {repr(self.name)}, {repr(self.children[0])})"

class UnaryExpression(Expression):
    def __init__(self, operator, operand):
        super().__init__()
        self.operator = operator
        self.add_child(operand)

    def __str__(self) -> str:
        return f"{self.operator}{self.children[0]}"
    
    def __repr__(self):
        return f"unary_expression({repr(self.operator)}, {repr(self.children[0])})"

class FunctionCall(Expression):
    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        self.arguments = arguments

    def __str__(self) -> str:
        return f"{self.name}({self.arguments})"
    
    def __repr__(self):
        return f"function_call({repr(self.name)}, {repr(self.arguments)})"
    
class InbuiltFunctionCall(Expression):
    def __init__(self, base, name, arguments):
        super().__init__()
        self.base = base
        self.name = name
        self.arguments = arguments

    def __str__(self) -> str:
        return f"{self.base}.{self.name}({self.arguments})"
    
    def __repr__(self):
        return f"inbuilt_function_call({repr(self.base)}, {repr(self.name)}, {repr(self.arguments)})"

class FunctionArgumentList(FunctionCall):
    def __init__(self):
        self.arguments = []

    def add_argument(self, argument):
        self.arguments.append(argument)

    def __str__(self) -> str:
        args = ", ".join(str(arg) for arg in self.arguments)
        return f"({args})"
    
    def __repr__(self):
        return f"function_argument_list({repr(self.arguments)})"

class FunctionArgument(FunctionArgumentList):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)
    
    def __repr__(self):
        return f"function_argument({repr(self.expression)})"

class Identifier(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self):
        return f"identifier({repr(self.name)})"

class Index(Expression):
    def __init__(self, expressions):
        super().__init__()
        self.expressions = expressions

    def __str__(self) -> str:
        return "".join(f"[{expr}]" for expr in self.expressions)
    
    def __repr__(self):
        return f"index({repr(self.expressions)})"

class Literal(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value.value
        self.type = value.type

    def __str__(self) -> str:
        return f"{self.value}"
    
    def __repr__(self):
        return f"literal({repr(self.value)})"
    
class Operator(Expression):
    def __init__(self, operator):
        super().__init__()
        self.operator = operator

    def __str__(self) -> str:
        return self.operator
    
    def __repr__(self):
        return f"operator({repr(self.operator)})"
    
class UnaryOperator(Expression):
    def __init__(self, operator):
        super().__init__()
        self.operator = operator

    def __str__(self) -> str:
        return self.operator
    
    def __repr__(self):
        return f"unary_operator({repr(self.operator)})"
    
class Comparator(Expression):
    def __init__(self, comparator):
        super().__init__()
        self.comparator = comparator

    def __str__(self) -> str:
        return self.comparator
    
    def __repr__(self):
        return f"comparator({repr(self.comparator)})"
    
class PrintStatement(ASTNode):
    def __init__(self, arguments):
        self.arguments = arguments

    def __str__(self) -> str:
        return f"print({self.arguments})"
    
    def __repr__(self):
        return f"print_statement({repr(self.arguments)})"

class PrintArgumentList(ASTNode):
    def __init__(self):
        self.arguments = []

    def add_argument(self, argument):
        self.arguments.append(argument)

    def __str__(self) -> str:
        args = ", ".join(str(arg) for arg in self.arguments)
        return f"({args})"
    
    def __repr__(self):
        return f"print_argument_list({repr(self.arguments)})"

class PrintArgument(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)
    
    def __repr__(self):
        return f"print_argument({repr(self.expression)})"
    
class Transformer(lark.Transformer):

    def __init__(self):
        self.temp_args = []
        self.args_list = PrintArgumentList()
        self.args_list_function = FunctionArgumentList()

    def print(self, children):
        log.debug(f"Processing 'print' with {children}")
        return (children[2])

    def print_args(self, children):
        log.debug(f"Processing 'print_args' with {children}")
        return children[0]

    def print_args_temp(self, children):
        log.debug(f"Processing 'print_args_temp' with {children}")
        if len(children) > 1:
            self.temp_args.append(children[1])
        if len(children) > 2:
            return children[2]
        else:
            return []

    def expression(self, children):
        log.debug(f"Processing 'expression' with {children}")
        return children

    def statement(self, children):
        log.debug(f"Processing 'statement' with {children}")
        return children[0]

    def statements(self, children):
        log.debug(f"Processing 'statements' with {children}")
        stmts = Statements()
        for child in children:
            stmts.append(child)
        return stmts
    
    def declare(self, children):
        log.debug(f"Processing 'declare' with {children}")
        return children[0]
    
    def tuple_declaration(self, children):
        log.debug(f"Processing Tuple Declaration with {children}")
        return Declaration(children[0], children[1], children[3])

    def list_declaration(self, children):
        log.debug(f"Processing List Declaration with {children}")
        return Declaration(children[0], children[1], children[3])

    def arr_declaration(self, children):
        log.debug(f"Processing Array Declaration with {children}")
        return Declaration(children[0], children[1], children[3])

    def exception_declaration(self, children):
        log.debug(f"Processing Exception Declaration with {children}")
        return ExceptionDeclaration(children[0], children[1], children[3])

    def variable_declaration(self, children):
        log.debug(f"Processing Variable Declaration with {children}")
        declaration_type = children[0]
        identifiers = []
        ind = -1
        for i in range(1, len(children), 2):
            if children[i-1].value == '=':
                ind = i
                break
            identifiers.append(children[i])
        expressions = []
        for i in range(ind, len(children), 2):
            expressions.append(children[i])
        log.debug(f"Variable Declaration - {declaration_type}, {identifiers}, {expressions}")
        return VariableDeclaration(declaration_type, identifiers, expressions)

    def matrix(self, children):
        return Matrix(children[0])

    def matrix_temp(self, children):
        matrix_list = MatrixList()
        for item in children:
            if isinstance(item, Matrix):
                matrix_list.add_item(item)
        return matrix_list

    def list_content(self, children):
        matrix_expression_list = MatrixExpressionList()
        for item in children:
            if isinstance(item, Expression):
                matrix_expression_list.add_expression(item)
        return matrix_expression_list
    
    def exception_declaration(self, args):
        log.debug(f"Processing Exception Declaration with {args}")
        return ExceptionDeclaration(args[0], args[1], args[3])
    
    def exception_handling(self, args):
        log.debug(f"Processing Exception Handling with {args}")
        return args[0]
    
    def try_catch_finally(self, args):
        log.debug(f"Processing Try Catch Finally with {args}")
        return TryCatchFinally(args[1], args[4], args[5], args[7], args[9])
    
    def block(self, args):
        log.debug(f"Processing Block with {args}")
        if len(args) == 2:
            return Block()
        return Block(args[1])
    
    def throw(self, args):
        log.debug(f"Processing Throw with {args}")
        return Throw(args[1], args[3])
    
    def return_statement(self, args):
        log.debug(f"Processing Return with {args}")
        if len(args) == 2:
            return Return()
        return Return(args[1])
    
    def control(self, args):
        log.debug(f"Processing Control with {args}")
        return args[0]
    
    def function(self, args):
        log.debug(f"Processing Function with {args}")
        return Function(args[1], args[3], args[5])
    
    def parameters(self, args):
        log.debug(f"Processing Parameters with {args}")
        parameters = Parameters()
        for i in range(0, len(args), 2):
            parameters.add_parameter(args[i])
        return parameters

    def parameter(self, args):
        log.debug(f"Processing Parameter with {args}")
        return Parameter(args[0], args[1])
    
    def if_else(self, children):
        expression = children[2]
        if_block = children[4]
        else_block = children[5] if children[5] else None
        return IfElse(expression, if_block, else_block)
    
    def else_temp(self, args):
        log.debug(f"Processing Else Temp with {args}")
        if args:
            return args[1]
        return None
    
    def while_(self, args):
        log.debug(f"Processing While with {args}")
        return While(args[2], args[4])
    
    def do_while(self, args):
        log.debug(f"Processing Do While with {args}")
        return DoWhile(args[1], args[4])
    
    def for_loop(self, args):
        log.debug(f"Processing For Loop with {args}")
        return ForLoop(args[2], args[4], args[6], args[8])
    
    def for_update(self, args): 
        log.debug(f"Processing For Update with {args}")
        return args[0]
    
    def break_continue(self, args):
        log.debug(f"Processing Break Continue with {args}")
        return args[0]
    
    def dec_control_flow(self, args):
        log.debug(f"Processing Dec Control Flow with {args}")
        return Declaration(args[0], args[1], args[3])
    
    def expression_statement(self, args):
        log.debug(f'expression_statement - {args}')
        return args[0]
    
    def expression(self, children):
        log.debug(f'expression - {children}')
        if hasattr(children[0], 'value') and children[0].value == '(' and hasattr(children[-1], 'value') and children[-1].value == ')':
            return self.expression(children[1:-1])
        if len(children) == 1:
            return children[0]
        elif len(children) == 3:  # binary operation
            operator = children[1]
            return BinaryOp(operator, children[0], children[2])
        elif len(children) == 2:  # unary expression
            operator = children[0]
            return UnaryExpression(operator, children[1])
        elif len(children) == 4:  # function call
            function_name = children[0]
            arguments = children[2]
            return FunctionCall(function_name, arguments)
        elif len(children) == 5:  # identifier with index
            identifier = children[0]
            index = children[2]
            return Index(identifier, index)

    def IDENTIFIER(self, token):
        log.debug(f'IDENTIFIER - {token}')
        return Identifier(token.value)

    def literal(self, children):
        log.debug(f'literal - {children}')
        return Literal(children[0])

    def index(self, children):
        log.debug(f'index - {children}')
        expressions = []
        for child in children:
            if isinstance(child, Expression):
                expressions.append(child)
        return Index(expressions)
    
    def assignment(self, children):
        return Assignment(children[0], children[2])
    
    def binary_op(self, children):
        log.debug(f'binary_op - {children}')
        return BinaryOp(children[1], children[0], children[2])
    
    def binary_comp(self, children):
        log.debug(f'binary_comp - {children}')
        return BinaryOp(children[1], children[0], children[2])
    
    def binary_compound_op(self, children):
        log.debug(f'binary_compound_op - {children}')
        return BinaryOp(children[1], children[0], children[2])
    
    def binary_dot_op(self, children):
        log.debug(f'binary_dot_op - {children}')
        return BinaryDotOp(children[0], children[2], children[3])
    
    def unary_expression(self, children):
        log.debug(f'unary_expression - {children}')
        if len(children) == 2:
            return UnaryExpression(children[0], children[1])
        else:
            return UnaryExpression(children[0], children[2])
        
    def function_call(self, children):
        log.debug(f'function_call - {children}')
        self.args_list_function = FunctionArgumentList()
        return FunctionCall(children[0], children[2])
    
    def inbuilt_function_call(self, children):
        log.debug(f'inbuilt_function_call - {children}')
        self.args_list_function = FunctionArgumentList()
        return InbuiltFunctionCall(children[0], children[2], children[4])
    
    def argument_temp(self, children):
        log.debug(f'argument_temp - {children}')
        if children:
            for i in range(0, len(children), 2):
                self.args_list_function.add_argument(children[i])
        return self.args_list_function
    
    def OPERATOR(self, token):
        return Operator(token.value)
    
    def COMPARATOR(self, token):
        return Comparator(token.value)
    
    def UNARY_OPERATOR(self, token):
        return UnaryOperator(token.value)
    
    def COMPOUND_OPERATOR(self, token):
        return Operator(token.value)
    
    def BREAK_CONTINUE(self, token):
        return BreakContinue(token.value)

    def print(self, children):
        log.debug(f'print - {children}')
        self.args_list = PrintArgumentList()
        return PrintStatement(children[2])

    def print_args(self, children):
        log.debug(f'print_args - {children}')
        if children:
            for i in range(0, len(children), 2):
                self.args_list.add_argument(children[i])
        return self.args_list
    
    def VARIABLE_DECLARATION(self, token):
        return DeclarationVariable(token.value)
    
    def LIST_DECLARATION(self, token):
        return DeclarationVariable(token.value)
    
    def ARR_DECLARATION(self, token):
        return DeclarationVariable(token.value)
    
    def TUPLE_DECLARATION(self, token):
        return DeclarationVariable(token.value)
    
transformer = Transformer()

def visualize_ast(node, indent="", last=True):
    if isinstance(node, list):
        for idx, item in enumerate(node):
            if idx == len(node) - 1:
                visualize_ast(item, indent, last=True)
            else:
                visualize_ast(item, indent, last=False)
        return
    
    prefix = "└── " if last else "├── "
    node_repr = repr(node) if hasattr(node, '__repr__') else str(node)
    print(indent + prefix + node_repr)
    child_indent = indent + ("   " if last else "│  ")
    if not hasattr(node, '__dict__'):
        return 
    children = [(k, v) for k, v in node.__dict__.items() if not k.startswith('_') and v]
    for idx, (attr, child) in enumerate(children):
        is_last = idx == len(children) - 1
        visualize_ast(child, child_indent, last=is_last)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parsing_ast.py <source_file>")
        sys.exit(1)
    source_file = sys.argv[1]
    with open(source_file) as f:
        source_code = f.read()
    tree = parser.parse(source_code)
    ast = transformer.transform(tree)
    visualize_ast(ast)

