# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Chunk, make_windows, normalize, read_text, split_sentences  # noqa: F401
# --- the listing ---
def build_chunks(paths: list[str]) -> list[Chunk]:
    texts = [(p, read_text(p)) for p in paths]                # весь корпус в памяти
    normalized = [(p, normalize(t)) for p, t in texts]        # ещё одна копия
    sentences = [s for p, t in normalized for s in split_sentences(p, t)]
    windows = make_windows(sentences, size=5, overlap=1)      # и ещё одна
    return [Chunk.from_sentences(w) for w in windows]
