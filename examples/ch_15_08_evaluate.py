# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored  # noqa: F401
# --- the listing ---
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True, slots=True)
class Case:
    question: str
    relevant: frozenset[str]
    kind: Literal["simple", "single", "multi"]

def recall_at_k(hits: list[Scored], relevant: frozenset[str], k: int) -> float:
    if not relevant:
        return 1.0
    found = {h.chunk.id for h in hits[:k]} & relevant
    return len(found) / len(relevant)

def reciprocal_rank(hits: list[Scored], relevant: frozenset[str]) -> float:
    for position, hit in enumerate(hits, start=1):
        if hit.chunk.id in relevant:
            return 1.0 / position
    return 0.0
