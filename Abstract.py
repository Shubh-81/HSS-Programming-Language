import sys
from typing import Union, List
from dataclasses import dataclass

from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta

this_module = sys.modules[__name__]

class _Ast(ast_utils.Ast):
    # This will be skipped by create_transformer(), because it starts with an underscore
    pass

class _Statement(_Ast):
    # This will be skipped by create_transformer(), because it starts with an underscore
    pass

@dataclass
class Identifier(_Ast):
    name: str

@dataclass
class Literal(_Ast):
    value: Union[int, float, str, bool]

@dataclass
class IntegerConstant(Literal):
    value: int

@dataclass
class DecimalConstant(Literal):
    value: float

@dataclass
class StringLiteral(Literal):
    value: str

@dataclass
class BooleanLiteral(Literal):
    value: bool

@dataclass
class Operator(_Ast):
    operator: str

@dataclass
class CompoundOperator(_Ast):
    operator: str

@dataclass
class UnaryOperator(_Ast):
    operator: str

@dataclass
class Comparator(_Ast):
    comparator: str

@dataclass
class Keyword(_Ast):
    keyword: str

@dataclass
class Operand(_Ast):
    pass

@dataclass
class IdentifierOperand(Operand):
    identifier: Identifier

@dataclass
class LiteralOperand(Operand):
    literal: Literal

@dataclass
class Expression(_Ast):
    pass

class UnaryExpression(Expression):
    operator: Operator
    operand: Operand

class BinaryExpression(Expression):
    operator: Operator
    left: Union[Expression, Operand]
    right: Union[Expression, Operand]

class FunctionCall(Expression):
    name: str
    
    
