import asyncio
from collections.abc import AsyncIterator

async def with_backpressure(source: AsyncIterator[str],
                            capacity: int = 8) -> AsyncIterator[str]:
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=capacity)

    async def pump() -> None:
        try:
            async for part in source:
                await queue.put(part)          # waits when the queue is full
        finally:
            await queue.put(None)              # end-of-stream marker

    async with asyncio.TaskGroup() as group:
        group.create_task(pump())
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
