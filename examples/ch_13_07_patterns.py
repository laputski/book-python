# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Answer, call_tool, merge, payload  # noqa: F401
# ─── листинг ───
from typing import Any


async def _excerpt() -> Any:
    match payload:
        case {"tool": str(name), "args": dict(args)}:      # проверка типов внутри
            return call_tool(name, args)
        case {"answer": str(text), **rest} if not rest:    # никаких иных ключей
            return Answer(text=text)
        case [first, *others]:                             # непустая последовательность
            return merge(first, others)
        case _:
            raise ValueError("неизвестная форма ответа")
