# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import freshness, index  # noqa: F401
# --- the listing ---
import numpy as np

queries = np.random.rand(32, 128).astype(np.float32)     # a batch of queries
matrix = index.matrix                                     # (N, 128)

scores = queries @ matrix.T          # (32, N): every query against every row
biased = scores - freshness[None, :] * 0.1   # (N,) broadcast across rows
