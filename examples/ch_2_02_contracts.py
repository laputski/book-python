# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored  # noqa: F401
# ─── листинг ───
from typing import Protocol

class Retriever(Protocol):
    """Источник кандидатов. Реализации не знают об этом протоколе."""

    async def retrieve(self, query: str, k: int) -> list[Scored]: ...

async def gather_candidates(sources: list[Retriever], query: str, k: int) -> list[list[Scored]]:
    return [await src.retrieve(query, k) for src in sources]
