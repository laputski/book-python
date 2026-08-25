# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored  # noqa: F401
# ─── листинг ───
from typing import Protocol, runtime_checkable

@runtime_checkable
class Retriever(Protocol):
    async def retrieve(self, query: str, k: int) -> list[Scored]: ...

class Broken:
    def retrieve(self):        # ни аргументов, ни асинхронности
        return None

isinstance(Broken(), Retriever)   # True: проверено лишь наличие имени
