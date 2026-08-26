# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Scored  # noqa: F401
# ─── листинг ───
def collapse_to_documents(hits: list[Scored]) -> list[Scored]:
    """Keeps each document's best chunk, ordered by descending score."""
    best: dict[str, Scored] = {}
    for hit in hits:
        current = best.get(hit.chunk.doc_id)
        if current is None or hit.score > current.score:
            best[hit.chunk.doc_id] = hit
    return sorted(best.values(), key=lambda h: -h.score)
