# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored, bm25_index  # noqa: F401
# ─── листинг ───
import asyncio

async def lexical_search(query: str, k: int) -> list[Scored]:
    # bm25_index.search is a synchronous call; push it onto a thread
    return await asyncio.to_thread(bm25_index.search, query, k)
