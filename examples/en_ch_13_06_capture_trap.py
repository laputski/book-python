# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import kind, module  # noqa: F401
# --- the listing ---
SIMPLE = "simple"

match kind:
    case SIMPLE:        # NOT a comparison with SIMPLE: a capture into a new name
        ...             # this branch always fires

match kind:
    case module.SIMPLE:  # a comparison: the dot makes the name a value
        ...
    case "simple":       # a comparison: a literal is a value
        ...
