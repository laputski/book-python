# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Chunk  # noqa: F401
# ─── листинг ───
import sys

def make_chunk(row: dict) -> Chunk:
    return Chunk(
        id=row["id"],
        doc_id=sys.intern(row["doc_id"]),      # few distinct values
        text=row["text"],                      # almost all distinct: do not pool
        context=sys.intern(row["context"]),    # repeats within a document
    )
