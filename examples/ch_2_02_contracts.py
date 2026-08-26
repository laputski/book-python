# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored  # noqa: F401
# --- the listing ---
from typing import Protocol

class Retriever(Protocol):
    """Источник кандидатов. Реализации не знают об этом протоколе."""

    async def retrieve(self, query: str, k: int) -> list[Scored]: ...

async def gather_candidates(sources: list[Retriever], query: str, k: int) -> list[list[Scored]]:
    return [await src.retrieve(query, k) for src in sources]
