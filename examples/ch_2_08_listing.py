# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Protocol, Scored  # noqa: F401
# ─── листинг ───
class Retriever(Protocol):
    async def retrieve(self, query: str, k: int, /) -> list[Scored]: ...
    #                                            ↑ дальше только по позиции
