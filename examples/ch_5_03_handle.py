# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DegradedSearch, SourceError, fan_out, k, log, query, sources  # noqa: F401
# --- the listing ---
from typing import Any


async def _excerpt() -> Any:
    try:
        try:
            results = await fan_out(sources, query, k)
        except* SourceError as group:
            failed = [exc.source for exc in group.exceptions if isinstance(exc, SourceError)]
            log.warning("источники отказали: %s", ", ".join(failed))
            raise DegradedSearch(failed) from group
    except TimeoutError:
        results = []                                   # бюджет исчерпан целиком
