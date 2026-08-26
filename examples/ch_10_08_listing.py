# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import matrix, np, queries  # noqa: F401
# --- the listing ---
scores = queries @ matrix.T          # транспонирование бесплатно, копия внутри
# при многократном повторении хранят заранее подготовленное расположение:
matrix_t = np.ascontiguousarray(matrix.T)
scores = queries @ matrix_t          # копирования нет
