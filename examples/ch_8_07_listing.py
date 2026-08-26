# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import HYDE_PROMPT, hashlib  # noqa: F401
# --- the listing ---
PROMPT_VERSION = hashlib.blake2b(HYDE_PROMPT.encode("utf-8"),
                                 digest_size=6).hexdigest()
