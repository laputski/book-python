# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Answer, RerankerUnavailable, SourceUnavailable, compose, fan_out, healthy_only, rerank, sources  # noqa: F401
# --- the listing ---
async def handle(question: str) -> Answer:
    degraded: list[str] = []
    try:
        candidates = await fan_out(sources, question, k=20)
    except* SourceUnavailable as group:
        degraded += [exc.source for exc in group.exceptions if isinstance(exc, SourceUnavailable)]
        candidates = await fan_out(healthy_only(sources), question, k=20)

    try:
        ranked = await rerank(question, candidates)
    except RerankerUnavailable:
        degraded.append("reranker")
        ranked = candidates                     # fusion order as the fallback

    return await compose(question, ranked, degraded=degraded)
