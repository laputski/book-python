from collections.abc import Sequence
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Ranked[T]:
    """A ranked list of anything: chunks, paths, entities."""
    items: tuple[T, ...]
    scores: tuple[float, ...]

def top[T](ranked: Ranked[T], n: int) -> Sequence[T]:
    return ranked.items[:n]
