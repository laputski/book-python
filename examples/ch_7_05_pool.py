import asyncio
from collections.abc import AsyncIterator, Callable, Awaitable
from contextlib import asynccontextmanager
from typing import Protocol

class Closeable(Protocol):
    async def aclose(self) -> None: ...

class Pool[C: Closeable]:
    def __init__(self, factory: Callable[[], Awaitable[C]], size: int = 8) -> None:
        self._factory = factory
        self._free: asyncio.LifoQueue[C] = asyncio.LifoQueue(maxsize=size)
        self._created = 0
        self._size = size
        self._guard = asyncio.Lock()

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[C]:
        conn = await self._take()
        broken = False
        try:
            yield conn
        except ConnectionError:
            broken = True
            raise
        finally:
            if broken:
                await self._discard(conn)
            else:
                self._free.put_nowait(conn)

    async def _discard(self, conn: C) -> None:
        self._created -= 1               # место освободилось для нового соединения
        await conn.aclose()

    async def _take(self) -> C:
        if not self._free.empty():
            return self._free.get_nowait()
        async with self._guard:
            if self._created < self._size:
                self._created += 1
                return await self._factory()
        return await self._free.get()          # ждём освобождения чужого
