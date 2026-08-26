# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import HYDE_PROMPT, model  # noqa: F401
# ─── листинг ───
from functools import lru_cache

@lru_cache(maxsize=4096)
async def hypothetical(question: str) -> str:
    return await model.complete(HYDE_PROMPT.format(question=question))
