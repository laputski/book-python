# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import graph, pool, tracer  # noqa: F401
# ─── листинг ───
from typing import Any


async def _excerpt() -> Any:
    conn = await pool.acquire()
    try:
        tx = await graph.begin()
        try:
            span = tracer.start("search")
            try:
                ...                       # the body ends up four levels deep
            finally:
                span.end()
        finally:
            await tx.rollback()
    finally:
        await pool.release(conn)
