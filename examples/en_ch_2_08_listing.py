# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Protocol, Scored  # noqa: F401
# --- the listing ---
class Retriever(Protocol):
    async def retrieve(self, query: str, k: int, /) -> list[Scored]: ...
    #                                            ↑ positional-only from here back
