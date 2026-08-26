# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import bias, scores, weights  # noqa: F401
# --- the listing ---
import numpy as np

out = np.empty_like(scores)
np.multiply(scores, weights, out=out)     # результат пишется в готовый массив
np.add(out, bias, out=out)                # и обновляется на месте
