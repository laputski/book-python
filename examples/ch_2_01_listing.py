# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored  # noqa: F401
# --- the listing ---
from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...

class ColbertRetriever(BaseRetriever):     # обязан знать про BaseRetriever
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...
