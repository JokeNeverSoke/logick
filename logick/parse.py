from __future__ import annotations

from lark import Lark, Transformer

from . import gates as g
from .controller import Controller

OPERATORS = {
    "AND": g.AND,
    "OR": g.OR,
    "XOR": g.XOR,
    "NOT": g.NOT,
    "NAND": g.NAND,
    "NOR": g.NOR,
}

PARSER = Lark(
    r"""
    ?start: expression
    expression: two_operation
        | one_operation
        | INPUT
        | "(" expression ")"
    two_operation: expression TWO_OPERATOR one_operation
        | expression TWO_OPERATOR INPUT
        | expression TWO_OPERATOR "(" expression ")"
    one_operation: ONE_OPERATOR INPUT
        | ONE_OPERATOR "(" expression ")"
    ONE_OPERATOR: "NOT"
    TWO_OPERATOR: "AND" | "OR" | "XOR" | "NAND" | "NOR" 
    INPUT: /[A-Z]/

    %import common.WS
    %ignore WS
    """,
    start="start",
)


class LogicTransformer(Transformer):
    def INPUT(self, args: list[str]) -> g.INPUT:
        name = args[0]
        return g.INPUT(name)

    def ONE_OPERATOR(self, args: str) -> g.Gate:
        return OPERATORS[args]

    def one_operation(self, args: tuple[type, g.Gate]) -> g.Gate:
        return args[0](args[1])

    def TWO_OPERATOR(self, args: str) -> g.Gate:
        return OPERATORS[args]

    def two_operation(self, args: tuple[g.Gate, type, g.Gate]) -> g.Gate:
        return args[1](args[0], args[2])

    def expression(self, args: tuple[g.Gate]) -> g.Gate:
        return args[0]


def parse(statement: str):
    """Parse logic string into structured gate into list of gates

    Inputs must be capital letters
    """
    tree = PARSER.parse(statement)
    tf = LogicTransformer()
    out: g.Gate = tf.transform(tree)
    return out
