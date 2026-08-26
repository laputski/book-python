# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DraftScore  # noqa: F401
# --- the listing ---
import json
from collections.abc import AsyncIterator

from pydantic import ValidationError

def close_brackets(fragment: str) -> str:
    """Completes the unclosed brackets so the fragment becomes parseable."""
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
        for item in items[emitted:len(items) - 1]:   # the last is still being written
            try:
                yield DraftScore.model_validate(item)
                emitted += 1
            except ValidationError:
                break
