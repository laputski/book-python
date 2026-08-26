# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import embed_one  # noqa: F401
# --- the listing ---
import numpy as np

class Vector:
    """An embedding computed on first access and remembered."""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = "_" + name          # where to store the computed value

    def __get__(self, obj: "Chunk | None", owner: type) -> "Vector | np.ndarray":
        if obj is None:
            return self                  # access through the class, not an instance
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
