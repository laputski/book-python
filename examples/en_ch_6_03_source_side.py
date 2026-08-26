# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Prompt  # noqa: F401
# ─── листинг ───
from collections.abc import AsyncIterator

async def stream(self, prompt: Prompt) -> AsyncIterator[str]:
    connection = await self._open(prompt)
    try:
        async for chunk in connection:
            yield chunk.text
    finally:
        await connection.aclose()        # runs on GeneratorExit too
