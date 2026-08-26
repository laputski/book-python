# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Chunk  # noqa: F401
# --- the listing ---
import sys

def make_chunk(row: dict) -> Chunk:
    return Chunk(
        id=row["id"],
        doc_id=sys.intern(row["doc_id"]),      # немного различных значений
        text=row["text"],                      # почти все различны: не разделяем
        context=sys.intern(row["context"]),    # повторяется в пределах документа
    )
