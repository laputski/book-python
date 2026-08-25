# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import asyncio, dense, graph, hyde, k, lexical, query  # noqa: F401
# ─── листинг ───
from typing import Any


async def _excerpt() -> Any:
    results = await asyncio.gather(
        dense.retrieve(query, k),
        lexical.retrieve(query, k),
        graph.retrieve(query, k),
        hyde.retrieve(query, k),
        return_exceptions=True,
    )
    good = [r for r in results if not isinstance(r, Exception)]
