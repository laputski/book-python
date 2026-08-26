# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import HYDE_PROMPT, model  # noqa: F401
# --- the listing ---
from functools import lru_cache

@lru_cache(maxsize=4096)
async def hypothetical(question: str) -> str:
    return await model.complete(HYDE_PROMPT.format(question=question))
