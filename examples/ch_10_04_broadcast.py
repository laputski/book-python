# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import freshness, index  # noqa: F401
# --- the listing ---
import numpy as np

queries = np.random.rand(32, 128).astype(np.float32)     # пакет запросов
matrix = index.matrix                                     # (N, 128)

scores = queries @ matrix.T          # (32, N): все запросы против всех строк
biased = scores - freshness[None, :] * 0.1   # (N,) транслируется по строкам
