# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import matrix, np, queries  # noqa: F401
# ─── листинг ───
scores = queries @ matrix.T          # транспонирование бесплатно, копия внутри
# при многократном повторении хранят заранее подготовленное расположение:
matrix_t = np.ascontiguousarray(matrix.T)
scores = queries @ matrix_t          # копирования нет
