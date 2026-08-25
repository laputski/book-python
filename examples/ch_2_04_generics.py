from collections.abc import Sequence
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Ranked[T]:
    """Ранжированный список чего угодно: фрагментов, путей, сущностей."""
    items: tuple[T, ...]
    scores: tuple[float, ...]

def top[T](ranked: Ranked[T], n: int) -> Sequence[T]:
    return ranked.items[:n]
