# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DenseHit, Query, Scored  # noqa: F401
# --- the listing ---
from collections.abc import Sequence
from typing import Protocol

class Retriever(Protocol):
    async def retrieve(self, query: str, k: int) -> Sequence[Scored]: ...

class Wide:
    # Qualifies: accepts more, returns narrower.
    async def retrieve(self, query: str | Query, k: int = 10) -> list[DenseHit]: ...

class Narrow:
    # Does not qualify: demands Query, while the protocol promised to accept str.
    async def retrieve(self, query: Query, k: int) -> Sequence[Scored]: ...
