from typing import Protocol

class Described(Protocol):
    name: str                     # a mutable attribute: demands read and write

class ReadOnly(Protocol):
    @property
    def name(self) -> str: ...    # the ability to read is enough
