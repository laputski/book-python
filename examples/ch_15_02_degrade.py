# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Answer, RerankerUnavailable, SourceUnavailable, compose, fan_out, healthy_only, rerank, sources  # noqa: F401
# ─── листинг ───
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
        ranked = candidates                     # порядок слияния как запасной

    return await compose(question, ranked, degraded=degraded)
