# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import SENTINEL, asyncio, model, prompt  # noqa: F401
# ─── листинг ───
queue: asyncio.Queue[str] = asyncio.Queue()      # без ограничения

async def produce() -> None:
    async for part in model.stream(prompt):
        queue.put_nowait(part)                    # никогда не ждёт
    queue.put_nowait(SENTINEL)
