import numpy as np

def maxsim(query: np.ndarray, document: np.ndarray) -> float:
    """query has shape (Lq, D), document has shape (Ld, D); both are normalized."""
    similarity = query @ document.T          # (Lq, Ld): every pair of tokens
    return float(similarity.max(axis=1).sum())

def maxsim_batch(query: np.ndarray, flat: np.ndarray,
                 offsets: np.ndarray) -> np.ndarray:
    """Documents are laid end to end; offsets mark each one's borders."""
    similarity = query @ flat.T              # (Lq, total length)
    scores = np.empty(len(offsets) - 1, dtype=np.float32)
    for i in range(len(offsets) - 1):
        block = similarity[:, offsets[i]:offsets[i + 1]]
        scores[i] = block.max(axis=1).sum()
    return scores
