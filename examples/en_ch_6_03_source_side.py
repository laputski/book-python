# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Prompt  # noqa: F401
# --- the listing ---
from collections.abc import AsyncIterator

async def stream(self, prompt: Prompt) -> AsyncIterator[str]:
    connection = await self._open(prompt)
    try:
        async for chunk in connection:
            yield chunk.text
    finally:
        await connection.aclose()        # runs on GeneratorExit too
