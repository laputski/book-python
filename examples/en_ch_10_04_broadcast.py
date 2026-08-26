# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import freshness, index  # noqa: F401
# ─── листинг ───
import numpy as np

queries = np.random.rand(32, 128).astype(np.float32)     # a batch of queries
matrix = index.matrix                                     # (N, 128)

scores = queries @ matrix.T          # (32, N): every query against every row
biased = scores - freshness[None, :] * 0.1   # (N,) broadcast across rows
