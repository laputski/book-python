# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import matrix, np, queries  # noqa: F401
# ─── листинг ───
scores = queries @ matrix.T          # the transpose is free; a copy happens inside
# when repeated per query, keep a prepared layout instead:
matrix_t = np.ascontiguousarray(matrix.T)
scores = queries @ matrix_t          # no copying
