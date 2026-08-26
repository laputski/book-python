import numpy as np
from scipy.sparse import csr_matrix

def personalized_rank(adjacency: csr_matrix, seeds: np.ndarray,
                      alpha: float = 0.85, iterations: int = 30,
                      tolerance: float = 1e-6) -> np.ndarray:
    """The power method: repeated multiplication by the transition matrix."""
    out_degree = np.asarray(adjacency.sum(axis=1)).ravel()
    np.maximum(out_degree, 1.0, out=out_degree)
    transition = adjacency.multiply(1.0 / out_degree[:, None]).tocsr()

    restart = seeds / max(seeds.sum(), 1e-12)
    rank = restart.copy()
    for _ in range(iterations):
        updated = alpha * (transition.T @ rank) + (1.0 - alpha) * restart
        if np.abs(updated - rank).sum() < tolerance:
            return updated
        rank = updated
    return rank
