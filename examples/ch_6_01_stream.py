# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import find_sentence_end  # noqa: F401
# ─── листинг ───
from collections.abc import AsyncIterator

async def sentences(parts: AsyncIterator[str]) -> AsyncIterator[str]:
    """Собирает части ответа до границы предложения."""
    buffer = ""
    async for part in parts:
        buffer += part
        while (cut := find_sentence_end(buffer)) is not None:
            yield buffer[:cut + 1]
            buffer = buffer[cut + 1:].lstrip()
    if buffer:
        yield buffer
