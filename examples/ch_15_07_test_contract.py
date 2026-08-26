# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DenseRetriever, FakeRetriever, Retriever, SAMPLE_CORPUS, settings  # noqa: F401
# --- the listing ---
import os
from itertools import pairwise

import pytest

@pytest.fixture(params=["fake", "real"])
def retriever(request) -> Retriever:
    if request.param == "real":
        if not os.environ.get("RUN_INTEGRATION"):
            pytest.skip("настоящая служба не запрошена")
        return DenseRetriever(settings.url)
    return FakeRetriever(SAMPLE_CORPUS)

@pytest.mark.asyncio
async def test_respects_k(retriever: Retriever) -> None:
    hits = await retriever.retrieve("сегментация корпуса", k=3)
    assert len(hits) <= 3
    assert all(a.score >= b.score for a, b in pairwise(hits))
