# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Cited, attach_citations, model, prompt, retrieved, sentences  # noqa: F401
# --- the listing ---
from collections.abc import AsyncIterator
from contextlib import aclosing

async def answer(query: str) -> AsyncIterator[Cited]:
    async with aclosing(model.stream(prompt)) as parts:      # закрытие гарантировано
        async for sentence in sentences(parts):
            yield attach_citations(sentence, retrieved)
