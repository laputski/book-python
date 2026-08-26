# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Answer, call_tool, merge, payload  # noqa: F401
# --- the listing ---
from typing import Any


async def _excerpt() -> Any:
    match payload:
        case {"tool": str(name), "args": dict(args)}:      # type checks inside
            return await call_tool(name, args)
        case {"answer": str(text), **rest} if not rest:    # no other keys allowed
            return Answer(text=text)
        case [first, *others]:                             # a nonempty sequence
            return merge(first, others)
        case _:
            raise ValueError("unrecognized reply shape")
