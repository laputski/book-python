import asyncio
from collections.abc import AsyncGenerator, AsyncIterator

async def with_keepalive(source: AsyncGenerator[str, None],
                         every: float = 15.0) -> AsyncIterator[str]:
    """Подмешивает пустые сообщения, чтобы разрыв соединения обнаружился."""
    pending: asyncio.Task[str] | None = None
    try:
        while True:
            if pending is None:
                pending = asyncio.create_task(source.__anext__())
            done, _ = await asyncio.wait({pending}, timeout=every)
            if not done:
                yield ": ping\n\n"          # запись выявит разорванное соединение
                continue
            try:
                yield pending.result()
            except StopAsyncIteration:
                return
            finally:
                pending = None
    finally:
        if pending is not None:
            pending.cancel()
        await source.aclose()
