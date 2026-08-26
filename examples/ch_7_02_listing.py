# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import graph, pool, tracer  # noqa: F401
# --- the listing ---
from typing import Any


async def _excerpt() -> Any:
    conn = await pool.acquire()
    try:
        tx = await graph.begin()
        try:
            span = tracer.start("search")
            try:
                ...                       # тело оказалось на четвёртом уровне вложенности
            finally:
                span.end()
        finally:
            await tx.rollback()
    finally:
        await pool.release(conn)
