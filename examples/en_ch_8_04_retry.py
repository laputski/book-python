# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import ServiceUnavailable  # noqa: F401
# --- the listing ---
import asyncio, functools, random
from collections.abc import Callable, Awaitable

RETRYABLE = (TimeoutError, ConnectionError, ServiceUnavailable)

def with_retry[**P, R](attempts: int = 4, base: float = 0.2, cap: float = 4.0):
    def decorate(fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @functools.wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(attempts):
                try:
                    return await fn(*args, **kwargs)
                except RETRYABLE:
                    if attempt == attempts - 1:
                        raise
                    ceiling = min(cap, base * 2 ** attempt)
                    await asyncio.sleep(random.uniform(0.0, ceiling))
            raise AssertionError("unreachable")
        return wrapper
    return decorate
