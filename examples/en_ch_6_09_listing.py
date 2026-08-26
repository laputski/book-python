# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import AsyncIterator, Prompt, TransientModelError, aclosing, model  # noqa: F401
# ─── листинг ───
async def resilient_stream(prompt: Prompt, attempts: int = 2) -> AsyncIterator[str]:
    written = ""
    for attempt in range(attempts):
        try:
            async with aclosing(model.stream(prompt.continued(written))) as parts:
                async for part in parts:
                    written += part
                    yield part
            return
        except TransientModelError:
            if attempt == attempts - 1:
                raise
            # Continue from what is already written, not from scratch.
