# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Scored, search  # noqa: F401
# --- the listing ---
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    """Граница: тело запроса, пришедшее извне."""
    query: str = Field(min_length=1, max_length=4096)
    k: int = Field(default=20, ge=1, le=200)
    sources: list[str] = Field(default_factory=list)

async def handle(raw: dict) -> list[Scored]:
    request = SearchRequest.model_validate(raw)   # единственная проверка
    return await search(request.query, request.k, request.sources)
