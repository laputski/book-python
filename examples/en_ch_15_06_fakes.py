# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Chunk, Scored, SourceUnavailable  # noqa: F401
# --- the listing ---
class FakeRetriever:
    """A working implementation of the Retriever protocol over a dictionary."""

    def __init__(self, corpus: dict[str, str], fail_after: int | None = None) -> None:
        self._corpus = corpus
        self._calls = 0
        self._fail_after = fail_after

    async def retrieve(self, query: str, k: int) -> list[Scored]:
        self._calls += 1
        if self._fail_after is not None and self._calls > self._fail_after:
            raise SourceUnavailable("the fake failed as scripted")
        words = set(query.lower().split())
        hits = [
            Scored(chunk=Chunk(id=cid, doc_id=cid, text=text),
                   score=len(words & set(text.lower().split())) / max(len(words), 1),
                   source="fake")
            for cid, text in self._corpus.items()
        ]
        hits.sort(key=lambda h: -h.score)
        return [h for h in hits if h.score > 0][:k]
