# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored  # noqa: F401
# --- the listing ---
from typing import Protocol, runtime_checkable

@runtime_checkable
class Retriever(Protocol):
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...

class Broken:
    def retrieve(self):        # no arguments, no asynchrony
        return None

isinstance(Broken(), Retriever)   # True: only the name's presence was checked
