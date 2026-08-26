# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Fused, Scored  # noqa: F401
# --- the listing ---
import heapq
from collections.abc import Sequence

def reciprocal_rank_fusion(rankings: Sequence[Sequence[Scored]], k: int,
                           constant: int = 60,
                           weights: Sequence[float] | None = None) -> list[Fused]:
    """Вклад источника в оценку документа равен 1 / (constant + ранг)."""
    weights = weights or [1.0] * len(rankings)
    totals: dict[str, float] = {}
    origins: dict[str, list[str]] = {}
    for ranking, weight in zip(rankings, weights, strict=True):
        for rank, hit in enumerate(ranking, start=1):
            totals[hit.chunk.id] = totals.get(hit.chunk.id, 0.0) + weight / (constant + rank)
            origins.setdefault(hit.chunk.id, []).append(hit.source)
    best = heapq.nlargest(k, totals.items(), key=lambda kv: kv[1])
    return [Fused(chunk_id=cid, score=score, sources=origins[cid]) for cid, score in best]
