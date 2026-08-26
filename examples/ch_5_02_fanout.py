# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Retriever, Scored  # noqa: F401
# --- the listing ---
import asyncio
from collections.abc import Sequence

class SourceError(Exception):
    def __init__(self, source: str, cause: BaseException) -> None:
        super().__init__(f"источник {source} отказал: {cause}")
        self.source = source

async def guarded(name: str, retriever: Retriever,
                  query: str, k: int, gate: asyncio.Semaphore) -> list[Scored]:
    async with gate:
        try:
            return await retriever.retrieve(query, k)
        except asyncio.CancelledError:
            raise                                   # отмену пропускаем дальше
        except Exception as exc:
            raise SourceError(name, exc) from exc

async def fan_out(sources: dict[str, Retriever], query: str, k: int,
                  budget: float = 1.5, limit: int = 8) -> Sequence[list[Scored]]:
    gate = asyncio.Semaphore(limit)
    tasks: dict[str, asyncio.Task[list[Scored]]] = {}
    async with asyncio.timeout(budget):
        async with asyncio.TaskGroup() as group:
            for name, retriever in sources.items():
                tasks[name] = group.create_task(guarded(name, retriever, query, k, gate))
    return [task.result() for task in tasks.values()]
