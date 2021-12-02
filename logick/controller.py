from typing import Any

from .display import pt
from .gates import *


class KeyDict(dict[Gate, bool]):
    """Stores the state of the gates"""

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class TraceResults(dict[KeyDict, dict[Gate, bool]]):
    """Stores the results of the trace

    Get a corresponding item by passing a dict of inputs

    e.g.

    >>> results[{INPUT("A"): True, INPUT("B"): False}]
    """

    def __getitem__(self, __k: dict[INPUT, Any]):
        return super().__getitem__(KeyDict({k: bool(v) for k, v in __k.items()}))


def _o(state: Any):
    """Change state into readable output"""
    if isinstance(state, bool):
        return "1" if state else "0"
    elif isinstance(state, int):
        if state == 0:
            return "0"
        else:
            return "1"
    elif isinstance(state, str):
        return state
    elif isinstance(state, list):
        return [_o(s) for s in state]
    return str(state)


def create_combinations(n: int) -> list[tuple[bool]]:
    """
    Create all possible combinations of n inputs
    """
    combinations = []
    for i in range(2 ** n):
        combination = []
        for j in range(n):
            combination.append(bool(i & (1 << j)))
        combinations.append(tuple(combination[::-1]))
    return combinations


def create_input_combinations(terminals: list[INPUT]) -> list[KeyDict]:
    combs = create_combinations(len(terminals))
    return [
        KeyDict({terminals[i]: comb[i] for i in range(len(terminals))})
        for comb in combs
    ]


class Controller:
    """The controller class, used to map out a truth table for a logic expression"""

    def __init__(self, outputs: list[Gate]):
        self.outputs = outputs
        terminal_inputs: list[INPUT] = []
        for output in outputs:
            terminal_inputs.extend(output.find_terminal_inputs())
        self.terminal_inputs = terminal_inputs
        self.unique_terminal_inputs = sorted(list(set(terminal_inputs)))

    def get_trace(self, **kwargs):
        in_out_table: dict[KeyDict, dict[Gate, bool]] = {}

        # create matrix of possible inputs
        inputs = create_input_combinations(self.unique_terminal_inputs)

        # traverse all possible inputs and save outputs
        for i in inputs:
            # set inputs
            for terminal in self.terminal_inputs:
                terminal.current = i[terminal]

            # save outputs
            out = {o: o(**kwargs) for o in self.outputs}
            in_out_table[i] = out
        return TraceResults(in_out_table)

    def display(self, **kwargs):
        """Prints the truth table of the controller's outputs"""
        # create table using `get_string_table`
        i_o = list(self.get_trace().items())

        headings = [str(i) for i in self.unique_terminal_inputs]
        # append outputs column heading
        headings.extend(str(o)[1:-1] for o in self.outputs)

        rows = []
        for line in i_o:
            row = line[0]
            row = [_o(row[i]) for i in self.unique_terminal_inputs]
            outputs = line[1]
            row.extend(_o(i) for i in outputs.values())
            rows.append(row)
        pt(rows, headings)
