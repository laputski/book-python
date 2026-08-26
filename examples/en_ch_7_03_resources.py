# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import GraphStore, Scored, graph, pool, run_search, temporary_file, tracer  # noqa: F401
# --- the listing ---
from contextlib import AsyncExitStack, asynccontextmanager

@asynccontextmanager
async def graph_transaction(graph: GraphStore):
    tx = await graph.begin()
    try:
        yield tx
        await tx.commit()
    except BaseException:
        await tx.rollback()
        raise

async def search(query: str, *, dump: bool = False) -> list[Scored]:
    async with AsyncExitStack() as stack:
        conn = await stack.enter_async_context(pool.acquire())
        tx = await stack.enter_async_context(graph_transaction(graph))
        stack.enter_context(tracer.span("search"))
        # A resource acquired conditionally does not complicate the release.
        dump_to = stack.enter_context(temporary_file()) if dump else None
        return await run_search(conn, tx, query, dump_to=dump_to)
