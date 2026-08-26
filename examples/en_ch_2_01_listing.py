# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored  # noqa: F401
# ─── листинг ───
from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...

class ColbertRetriever(BaseRetriever):     # must know about BaseRetriever
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...
