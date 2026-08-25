import numpy as np

def maxsim(query: np.ndarray, document: np.ndarray) -> float:
    """query имеет форму (Lq, D), document форму (Ld, D); оба нормированы."""
    similarity = query @ document.T          # (Lq, Ld): все пары элементов
    return float(similarity.max(axis=1).sum())

def maxsim_batch(query: np.ndarray, flat: np.ndarray,
                 offsets: np.ndarray) -> np.ndarray:
    """Документы уложены подряд; offsets задаёт границы каждого."""
    similarity = query @ flat.T              # (Lq, сумма длин)
    scores = np.empty(len(offsets) - 1, dtype=np.float32)
    for i in range(len(offsets) - 1):
        block = similarity[:, offsets[i]:offsets[i + 1]]
        scores[i] = block.max(axis=1).sum()
    return scores
