# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import DenseHit, Query, Scored  # noqa: F401
# ─── листинг ───
from collections.abc import Sequence
from typing import Protocol

class Retriever(Protocol):
    async def retrieve(self, query: str, k: int) -> Sequence[Scored]: ...

class Wide:
    # Годится: принимает больше, возвращает уже.
    async def retrieve(self, query: str | Query, k: int = 10) -> list[DenseHit]: ...

class Narrow:
    # Не годится: требует Query, а протокол обещал допускать str.
    async def retrieve(self, query: Query, k: int) -> Sequence[Scored]: ...
