from __future__ import annotations


def get_string_table(table: list[list[str]], headings: None | list[str] = None) -> str:
    """Consume table and create an ascii table

    If no headings are provided, the heading row would not be printed.

    Example return:
    +---------+---------+
    | a       | b       |
    +---------+---------+
    | 1       | 2       |
    | i justd | 1231244 |
    +---------+---------+
    """
    # assume height is 1 for all rows
    # get the needed width of each column
    widths: list[int] = [0] * len(table[0])
    for row in table:
        for i, col in enumerate(row):
            widths[i] = max(widths[i], len(col))
    # also reference heading lengths
    if headings:
        for i, col in enumerate(headings):
            widths[i] = max(widths[i], len(col))

    # build the string
    s: str = ""
    horizontal_line = "+" + "".join(["-" * (w + 2) + "+" for w in widths]) + "\n"
    s += horizontal_line
    if headings is not None:
        s += (
            "|"
            + "".join(
                [
                    " " + heading.ljust(widths[i]) + " |"
                    for i, heading in enumerate(headings)
                ]
            )
            + "\n"
        )
        s += horizontal_line

    for row in table:
        s += "|"
        for i, col in enumerate(row):
            s += " " + col.ljust(widths[i] + 1) + "|"
        s += "\n"
    s += horizontal_line

    return s


def pt(*args, **kwargs):
    print(get_string_table(*args, **kwargs), end="")
