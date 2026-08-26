# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import DenseIndex  # noqa: F401
# --- the listing ---
import numpy as np

def to_binary(vectors: np.ndarray) -> np.ndarray:
    """Один бит на измерение: знак числа. Форма (N, D) переходит в (N, D // 8)."""
    return np.packbits(vectors > 0, axis=1)

def hamming(codes: np.ndarray, query_code: np.ndarray) -> np.ndarray:
    """Число несовпавших битов для каждой строки."""
    return np.bitwise_count(codes ^ query_code).sum(axis=1)   # NumPy 2.0+

def search_two_stage(index: "DenseIndex", query: np.ndarray, k: int,
                     widen: int = 16) -> tuple[np.ndarray, np.ndarray]:
    distances = hamming(index.codes, to_binary(query[None, :])[0])
    candidates = np.argpartition(distances, k * widen)[:k * widen]
    exact = index.matrix[candidates] @ query        # переоценка по полному
    order = candidates[np.argsort(-exact)][:k]
    return order, index.matrix[order] @ query
