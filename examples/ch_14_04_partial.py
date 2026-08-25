# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import DraftScore  # noqa: F401
# ─── листинг ───
import json
from collections.abc import AsyncIterator

from pydantic import ValidationError

def close_brackets(fragment: str) -> str:
    """Достраивает незакрытые скобки, чтобы фрагмент стал разбираемым."""
    stack: list[str] = []
    in_string = escaped = False
    for ch in fragment:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in "[{":
            stack.append("]" if ch == "[" else "}")
        elif ch in "]}" and stack:
            stack.pop()
    trimmed = fragment if in_string else fragment.rstrip().rstrip(",")
    return trimmed + ('"' if in_string else "") + "".join(reversed(stack))

async def partial_scores(parts: AsyncIterator[str]) -> AsyncIterator[DraftScore]:
    buffer, emitted = "", 0
    async for part in parts:
        buffer += part
        try:
            data = json.loads(close_brackets(buffer))
        except json.JSONDecodeError:
            continue
        items = data.get("scores", [])
        for item in items[emitted:len(items) - 1]:   # последний ещё дописывается
            try:
                yield DraftScore.model_validate(item)
                emitted += 1
            except ValidationError:
                break
