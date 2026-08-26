# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import dense_hits, k, lexical_hits  # noqa: F401
# --- the listing ---
merged: dict[str, float] = {}
for hit in dense_hits:
    merged[hit.chunk.id] = merged.get(hit.chunk.id, 0.0) + 0.7 * hit.score
for hit in lexical_hits:
    merged[hit.chunk.id] = merged.get(hit.chunk.id, 0.0) + 0.3 * hit.score
best = sorted(merged.items(), key=lambda kv: -kv[1])[:k]
