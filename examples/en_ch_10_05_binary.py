# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import DenseIndex  # noqa: F401
# ─── листинг ───
import numpy as np

def to_binary(vectors: np.ndarray) -> np.ndarray:
    """One bit per dimension: the sign. Shape (N, D) becomes (N, D // 8)."""
    return np.packbits(vectors > 0, axis=1)

def hamming(codes: np.ndarray, query_code: np.ndarray) -> np.ndarray:
    """The count of mismatched bits for every row."""
    return np.bitwise_count(codes ^ query_code).sum(axis=1)   # NumPy 2.0+

def search_two_stage(index: "DenseIndex", query: np.ndarray, k: int,
                     widen: int = 16) -> tuple[np.ndarray, np.ndarray]:
    distances = hamming(index.codes, to_binary(query[None, :])[0])
    candidates = np.argpartition(distances, k * widen)[:k * widen]
    exact = index.matrix[candidates] @ query        # rescoring by the full form
    order = candidates[np.argsort(-exact)][:k]
    return order, index.matrix[order] @ query
