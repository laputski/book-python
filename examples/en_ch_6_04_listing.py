# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import SENTINEL, asyncio, model, prompt  # noqa: F401
# --- the listing ---
queue: asyncio.Queue[str] = asyncio.Queue()      # unbounded

async def produce() -> None:
    async for part in model.stream(prompt):
        queue.put_nowait(part)                    # never waits
    queue.put_nowait(SENTINEL)
