from .gates import *
from .parse import *
from .utils import inputs


def test_parsing():
    A, B, Z = inputs("A B Z")

    # inputs
    assert parse("A") == A
    assert parse("B") == B
    assert parse("Z") == Z

    # simple expressions
    assert parse("A AND A") == AND(A, A)
    assert parse("A NAND A") == NAND(A, A)
    assert parse("A OR A") == OR(A, A)
    assert parse("A NOR A") == NOR(A, A)
    assert parse("A XOR A") == XOR(A, A)
    assert parse("NOT A") == NOT(A)

    # left recursion order
    assert parse("A AND A OR A") == OR(AND(A, A), A)
    assert parse("A AND (A OR A)") == AND(A, OR(A, A))
    assert parse("A OR A AND (A)") == AND(OR(A, A), A)
    assert parse("A OR (A AND A)") == OR(A, AND(A, A))
    assert parse("NOT A AND B") == AND(NOT(A), B)
    assert parse("NOT (A AND B)") == NOT(AND(A, B))

    assert parse("A AND A AND A") == AND(AND(A, A), A)
    assert parse("A AND A AND A AND A") == AND(AND(AND(A, A), A), A)
    assert parse("A OR A OR A") == OR(OR(A, A), A)
    assert parse("A OR A OR A OR A") == OR(OR(OR(A, A), A), A)

    # super long expressions
    assert parse("A AND (B XOR Z) OR (NOT A NAND B)") == OR(
        AND(A, XOR(B, Z)), NAND(NOT(A), B)
    )

    assert parse("((((NOT A) NOR B) XOR A) AND B)") == AND(XOR(NOR(NOT(A), B), A), B)


def test_parse_tree():
    (A,) = inputs("A")

    u = parse("A AND A")
    trace = Controller([u]).get_trace()
    assert trace[{A: 0}] == {u: False}
    assert trace[{A: 1}] == {u: True}
