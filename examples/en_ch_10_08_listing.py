# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import matrix, np, queries  # noqa: F401
# --- the listing ---
scores = queries @ matrix.T          # the transpose is free; a copy happens inside
# when repeated per query, keep a prepared layout instead:
matrix_t = np.ascontiguousarray(matrix.T)
scores = queries @ matrix_t          # no copying
