# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DenseHit, LexicalHit, Scored  # noqa: F401
# --- the listing ---
from functools import singledispatch

@singledispatch
def normalize(hit: Scored) -> float:
    raise NotImplementedError(f"no rule for {type(hit).__name__}")

@normalize.register
def _(hit: DenseHit) -> float:
    return (hit.score + 1.0) / 2.0            # from [-1, 1] into [0, 1]

@normalize.register
def _(hit: LexicalHit) -> float:
    return hit.score / (hit.score + 1.0)      # squashing an unbounded scale
