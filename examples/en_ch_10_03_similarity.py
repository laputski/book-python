import numpy as np

class DenseIndex:
    def __init__(self, vectors: np.ndarray) -> None:
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        np.maximum(norms, 1e-12, out=norms)          # guard against a zero row
        self._matrix = np.ascontiguousarray(vectors / norms)

    def search(self, query: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        q = query.astype(np.float32, copy=False)
        q = q / max(float(np.linalg.norm(q)), 1e-12)
        scores = self._matrix @ q                    # (N, D) by (D,) gives (N,)
        if k >= scores.shape[0]:
            order = np.argsort(-scores)
        else:
            part = np.argpartition(-scores, k)[:k]   # selection without a full sort
            order = part[np.argsort(-scores[part])]
        return order, scores[order]
