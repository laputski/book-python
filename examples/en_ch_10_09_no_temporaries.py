# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import bias, scores, weights  # noqa: F401
# --- the listing ---
import numpy as np

out = np.empty_like(scores)
np.multiply(scores, weights, out=out)     # the result lands in a ready array
np.add(out, bias, out=out)                # and is updated in place
