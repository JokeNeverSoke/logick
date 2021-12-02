from _pytest.capture import CaptureFixture

from .controller import *
from .gates import *
from .utils import inputs


def test_tracing():
    A, B = inputs("A B")
    C = AND(A, B)
    c = Controller([C])
    trace = c.get_trace()

    assert trace[{A: 1, B: 1}] == {C: True}
    assert trace[{A: 0, B: 1}] == {C: False}
    assert trace[{A: 0, B: 1}] == trace[{A: 1, B: 0}]
    assert trace[{A: 0, B: 1}] != {C: True}
    assert trace[{A: 1, B: 1}] != trace[{A: 0, B: 0}]

    A, B, C, D = inputs("A B C D")
    E = AND(AND(AND(A, B), C), D)
    F = AND(AND(A, B), AND(C, D))
    c1 = Controller([E])
    c2 = Controller([F])
    trace1 = c1.get_trace()
    trace2 = c2.get_trace()

    assert trace1 != trace2

    C = AND(A, A)
    c = Controller([C])
    trace = c.get_trace()
    assert trace[{A: 1}] == {C: True}


def test_display(capsys: CaptureFixture):
    A, B = inputs("A B")
    C = AND(A, B)
    c = Controller([C])
    c.display()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """\
+---+---+---------+
| A | B | A AND B |
+---+---+---------+
| 0 | 0 | 0       |
| 0 | 1 | 0       |
| 1 | 0 | 0       |
| 1 | 1 | 1       |
+---+---+---------+
"""
    )

    C = AND(A, A)
    c = Controller([C])
    c.display()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """\
+---+---------+
| A | A AND A |
+---+---------+
| 0 | 0       |
| 1 | 1       |
+---+---------+
"""
    )
