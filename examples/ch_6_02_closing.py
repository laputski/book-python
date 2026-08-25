# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Cited, attach_citations, model, prompt, retrieved, sentences  # noqa: F401
# ─── листинг ───
from collections.abc import AsyncIterator
from contextlib import aclosing

async def answer(query: str) -> AsyncIterator[Cited]:
    async with aclosing(model.stream(prompt)) as parts:      # закрытие гарантировано
        async for sentence in sentences(parts):
            yield attach_citations(sentence, retrieved)
