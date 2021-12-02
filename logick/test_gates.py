from .gates import *
from .utils import inputs


def test_mechanism():
    A, B = inputs("A B")
    C = AND(A, B)
    A.current, B.current = True, True
    assert C() == True
    A.current, B.current = False, False
    assert C() == False
    A.current, B.current = True, False
    assert C() == False
    A.current, B.current = False, True
    assert C() == False

    C = AND(A, A)
    A.current = True
    assert C() == True
    A.current = False
    assert C() == False


def test_equality():
    # single input equality
    A, B, C = inputs("A B C")
    assert A == A
    assert A != B
    assert A != C
    assert (A, B) == (A, B)
    assert (A, B) != (B, A)

    # single gate equality
    assert AND(A, B) == AND(A, B)
    assert AND(A, B) != AND(A, C)
    assert NOT(A) == NOT(A)
    assert NOT(A) != NOT(B)

    # interchangability
    assert AND(A, B) == AND(B, A)
    assert AND(A, B) != AND(B, C)

    # different gates
    assert AND(A, B) != OR(A, B)
    assert AND(A, B) != XOR(A, B)
    assert AND(A, B) != NOR(A, B)
    assert AND(A, A) != NOT(A)
    assert NOT(A) != AND(A, A)

    # complex structures
    assert AND(AND(A, B), C) == AND(AND(A, B), C)
    assert AND(AND(A, B), C) != AND(AND(A, C), B)
    assert AND(AND(A, B), C) != AND(AND(B, C), A)

    assert AND(NOT(A), B) != AND(NOT(B), A)
    assert NOT(AND(A, B)) != AND(NOT(A), NOT(B))
    assert NOT(AND(A, B)) != NAND(A, B)


def test_str():
    A, B, C = inputs("A B C")

    # simple expressions
    assert str(A) == "A"
    assert str(AND(A, B)) == "(A AND B)"
    assert str(NAND(A, B)) == "(A NAND B)"
    assert str(OR(A, B)) == "(A OR B)"
    assert str(XOR(A, B)) == "(A XOR B)"
    assert str(NOR(A, B)) == "(A NOR B)"
    assert str(NOT(A)) == "(NOT A)"

    # complex expressions
    assert str(AND(AND(A, B), C)) == "((A AND B) AND C)"
    assert str(AND(NOT(A), XOR(C, B))) == "((NOT A) AND (C XOR B))"
    assert str(AND(NOT(A), NOT(B))) == "((NOT A) AND (NOT B))"
    assert str(NOT(AND(A, B))) == "(NOT (A AND B))"
