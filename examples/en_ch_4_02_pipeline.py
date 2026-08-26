# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Chunk, Sentence, normalize, read_text, split_sentences  # noqa: F401
# --- the listing ---
from collections.abc import Iterable, Iterator
from itertools import batched

def read_texts(paths: Iterable[str]) -> Iterator[tuple[str, str]]:
    for path in paths:
        yield path, normalize(read_text(path))

def to_sentences(docs: Iterable[tuple[str, str]]) -> Iterator[Sentence]:
    for doc_id, text in docs:
        yield from split_sentences(doc_id, text)      # delegation

def to_windows(sents: Iterable[Sentence], size: int = 5,
               overlap: int = 1) -> Iterator[Chunk]:
    buffer: list[Sentence] = []
    for sent in sents:
        buffer.append(sent)
        if len(buffer) == size:
            yield Chunk.from_sentences(buffer)
            buffer = buffer[size - overlap:]
    if buffer:
        yield Chunk.from_sentences(buffer)

def build_chunks(paths: Iterable[str], batch: int = 256) -> Iterator[tuple[Chunk, ...]]:
    return batched(to_windows(to_sentences(read_texts(paths))), batch)
