import asyncio, time

class RateLimiter:
    """Накопитель разрешений: пополняется равномерно, тратится по одному."""

    def __init__(self, rate: float, burst: int) -> None:
        self._rate = rate                # разрешений в секунду
        self._capacity = burst           # сколько можно накопить про запас
        self._tokens = float(burst)
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                self._tokens = min(self._capacity,
                                   self._tokens + (now - self._updated) * self._rate)
                self._updated = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                await asyncio.sleep((1.0 - self._tokens) / self._rate)
