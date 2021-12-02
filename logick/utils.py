from __future__ import annotations

from .gates import INPUT


def inputs(names: str | list[str]) -> list[INPUT]:
    """Returns a list of input gates from a list of names"""
    if isinstance(names, str):
        names = names.split()
    r = [INPUT(name.upper()) for name in names]
    return r
