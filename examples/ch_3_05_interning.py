# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Chunk  # noqa: F401
# ─── листинг ───
import sys

def make_chunk(row: dict) -> Chunk:
    return Chunk(
        id=row["id"],
        doc_id=sys.intern(row["doc_id"]),      # немного различных значений
        text=row["text"],                      # почти все различны: не разделяем
        context=sys.intern(row["context"]),    # повторяется в пределах документа
    )
