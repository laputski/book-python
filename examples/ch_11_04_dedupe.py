# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored  # noqa: F401
# --- the listing ---
def collapse_to_documents(hits: list[Scored]) -> list[Scored]:
    """Оставляет лучший фрагмент каждого документа, в порядке убывания оценки."""
    best: dict[str, Scored] = {}
    for hit in hits:
        current = best.get(hit.chunk.doc_id)
        if current is None or hit.score > current.score:
            best[hit.chunk.doc_id] = hit
    return sorted(best.values(), key=lambda h: -h.score)
