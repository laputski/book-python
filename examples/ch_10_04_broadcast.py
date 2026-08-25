# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import freshness, index  # noqa: F401
# ─── листинг ───
import numpy as np

queries = np.random.rand(32, 128).astype(np.float32)     # пакет запросов
matrix = index.matrix                                     # (N, 128)

scores = queries @ matrix.T          # (32, N): все запросы против всех строк
biased = scores - freshness[None, :] * 0.1   # (N,) транслируется по строкам
