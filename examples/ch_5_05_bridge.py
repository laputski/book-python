# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored, bm25_index  # noqa: F401
# --- the listing ---
import asyncio

async def lexical_search(query: str, k: int) -> list[Scored]:
    # bm25_index.search является синхронным вызовом; выносим его в поток
    return await asyncio.to_thread(bm25_index.search, query, k)
