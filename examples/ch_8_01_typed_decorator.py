# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import tracer  # noqa: F401
# ─── листинг ───
import functools
from collections.abc import Callable, Awaitable

def timed[**P, R](fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @functools.wraps(fn)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        with tracer.span(fn.__qualname__):
            return await fn(*args, **kwargs)
    return wrapper
