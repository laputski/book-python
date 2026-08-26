import asyncio
from collections import OrderedDict
from collections.abc import Awaitable, Callable

class SingleFlightCache[K, V]:
    """A cache in which simultaneous misses on one key await a single computation."""

    def __init__(self, capacity: int = 4096) -> None:
        self._done: OrderedDict[K, V] = OrderedDict()
        self._running: dict[K, asyncio.Future[V]] = {}
        self._capacity = capacity

    async def get(self, key: K, compute: Callable[[], Awaitable[V]]) -> V:
        if key in self._done:
            self._done.move_to_end(key)
            return self._done[key]
        if key in self._running:
            return await asyncio.shield(self._running[key])
        future: asyncio.Future[V] = asyncio.get_running_loop().create_future()
        self._running[key] = future
        try:
            value = await compute()
        except BaseException as exc:
            future.set_exception(exc)
            raise
        else:
            future.set_result(value)
            self._done[key] = value
            if len(self._done) > self._capacity:
                self._done.popitem(last=False)
            return value
        finally:
            self._running.pop(key, None)
