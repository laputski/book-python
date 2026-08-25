from typing import Protocol

class Described(Protocol):
    name: str                     # изменяемый атрибут: требует и чтения, и записи

class ReadOnly(Protocol):
    @property
    def name(self) -> str: ...    # достаточно возможности прочитать
