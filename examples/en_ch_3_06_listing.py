# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import dataclass, field  # noqa: F401
# --- the listing ---
@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    text: str = field(compare=False)      # takes part in neither comparison nor hash
    context: str = field(compare=False, default="")
