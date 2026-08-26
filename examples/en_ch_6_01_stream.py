# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import find_sentence_end  # noqa: F401
# --- the listing ---
from collections.abc import AsyncIterator

async def sentences(parts: AsyncIterator[str]) -> AsyncIterator[str]:
    """Accumulates answer fragments up to a sentence boundary."""
    buffer = ""
    async for part in parts:
        buffer += part
        while (cut := find_sentence_end(buffer)) is not None:
            yield buffer[:cut + 1]
            buffer = buffer[cut + 1:].lstrip()
    if buffer:
        yield buffer
