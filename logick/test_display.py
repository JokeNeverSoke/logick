from _pytest.capture import CaptureFixture

from .display import *


def test_display():
    assert (
        get_string_table(
            [
                ["a", "b", "c"],
                ["d", "e", "f"],
                ["g", "h", "i"],
            ]
        )
        == """\
+---+---+---+
| a | b | c |
| d | e | f |
| g | h | i |
+---+---+---+
"""
    )


def test_string_table_same_as_pt(capsys: CaptureFixture):
    table = [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"],
    ]
    pt(table)
    captured = capsys.readouterr()
    assert captured.out == get_string_table(table)
