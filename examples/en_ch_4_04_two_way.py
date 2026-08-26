# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Chunk  # noqa: F401
# --- the listing ---
from collections.abc import Generator

def adaptive_batcher(initial: int = 64) -> Generator[tuple[Chunk, ...], Chunk | int | None, int]:
    """Yields batches; accepts a chunk or a new batch size from outside."""
    size, total = initial, 0
    buffer: list[Chunk] = []
    while True:
        chunk = yield tuple(buffer) if len(buffer) >= size else ()
        if isinstance(chunk, int):        # the caller announced a new size
            size = max(1, chunk)
            continue
        if chunk is None:
            break
        buffer.append(chunk)
        if len(buffer) >= size:
            total += len(buffer)
            buffer.clear()
    return total
