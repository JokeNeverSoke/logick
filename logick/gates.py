class Gate:
    def __init__(self):
        pass

    def __call__(self, *args) -> bool:
        o = self.do(*args)
        return o

    def __repr__(self) -> str:
        return "<Gate>"

    def __str__(self):
        return "<Gate>"

    def __eq__(self, __o: object) -> bool:
        raise NotImplementedError

    def find_terminal_inputs(self) -> list["INPUT"]:
        """Find all terminal inputs, does not remove duplicates"""
        raise NotImplementedError

    def do(self, *args):
        raise NotImplementedError


class OneGate(Gate):
    a: Gate

    def __repr__(self):
        return f"<{type(self).__name__}({repr(self.a)})>"

    def __str__(self):
        return f"({type(self).__name__} {self.a})"

    def __hash__(self) -> int:
        return hash(f"gate-{type(self).__name__}-{hash(self.a)}")

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, OneGate):
            return False
        if type(self) != type(__o):
            return False
        return self.a == __o.a

    def find_terminal_inputs(self) -> list["INPUT"]:
        return self.a.find_terminal_inputs()


class TwoGate(Gate):
    a: Gate
    b: Gate

    def __repr__(self):
        return f"<{type(self).__name__}({repr(self.a)}, {repr(self.b)})>"

    def __str__(self):
        return f"({self.a} {type(self).__name__} {self.b})"

    def __hash__(self) -> int:
        return hash(f"gate-{type(self).__name__}-{hash(self.a)}-{hash(self.b)}")

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, TwoGate):
            return False
        if type(self) != type(__o):
            return False
        return (self.a == __o.a and self.b == __o.b) or (
            self.a == __o.b and self.b == __o.a
        )

    def find_terminal_inputs(self) -> list["INPUT"]:
        return self.a.find_terminal_inputs() + self.b.find_terminal_inputs()


class AND(TwoGate):
    def __init__(self, a: Gate, b: Gate):
        super().__init__()
        self.a = a
        self.b = b

    def do(self, **kwargs):
        return self.a(**kwargs) and self.b(**kwargs)


class OR(TwoGate):
    def __init__(self, a: Gate, b: Gate):
        super().__init__()
        self.a = a
        self.b = b

    def do(self, **kwargs):
        return self.a(**kwargs) or self.b(**kwargs)


class NOT(OneGate):
    def __init__(self, a: Gate):
        super().__init__()
        self.a = a

    def do(self, **kwargs):
        return not self.a(**kwargs)


class NAND(TwoGate):
    def __init__(self, a: Gate, b: Gate):
        super().__init__()
        self.a = a
        self.b = b

    def do(self, **kwargs):
        return not (self.a(**kwargs) and self.b(**kwargs))


class NOR(TwoGate):
    def __init__(self, a: Gate, b: Gate):
        super().__init__()
        self.a = a
        self.b = b

    def do(self, **kwargs):
        return not (self.a(**kwargs) or self.b(**kwargs))


class XOR(TwoGate):
    def __init__(self, a: Gate, b: Gate):
        super().__init__()
        self.a = a
        self.b = b

    def do(self, **kwargs):
        return self.a(**kwargs) != self.b(**kwargs)


class INPUT(Gate):
    def __init__(self, name: str):
        super().__init__()
        self.current: bool = False
        self.name = name

    def __repr__(self):
        return f"<INPUT {self.name}>"

    def __str__(self):
        return self.name

    def __hash__(self) -> int:
        return hash(f"gate-input-{self.name}")

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)

    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, INPUT):
            return False
        return self.name < __o.name

    def find_terminal_inputs(self) -> list["INPUT"]:
        return [self]

    def do(self, **kwargs):
        return self.current
