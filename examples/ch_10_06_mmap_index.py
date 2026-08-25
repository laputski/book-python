import numpy as np

index = np.memmap("vectors.f32", dtype=np.float32, mode="r", shape=(50_000_000, 128))

def score_shard(query: np.ndarray, start: int, stop: int) -> np.ndarray:
    block = np.asarray(index[start:stop])     # читается только этот участок
    return block @ query
