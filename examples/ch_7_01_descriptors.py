# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import embed_one  # noqa: F401
# ─── листинг ───
import numpy as np

class Vector:
    """Представление, вычисляемое при первом обращении и запоминаемое."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = "_" + name          # где хранить вычисленное

    def __get__(self, obj: "Chunk | None", owner: type) -> "Vector | np.ndarray":
        if obj is None:
            return self                  # обращение через класс, не через экземпляр
        cached = getattr(obj, self._name, None)
        if cached is None:
            cached = embed_one(obj.embedding_input)
            object.__setattr__(obj, self._name, cached)
        return cached

class Chunk:
    __slots__ = ("id", "text", "context", "_vector")
    id: str
    text: str
    context: str
    vector = Vector()

    @property
    def embedding_input(self) -> str:
        return f"{self.context}\n\n{self.text}" if self.context else self.text
