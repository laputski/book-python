import numpy as np

index = np.zeros((1_000_000, 128), dtype=np.float32)   # row-major order

index[42]          # 128 numbers in a row: one visit to a memory stretch
index[:, 42]       # a million numbers at a 512-byte stride: a visit each

index.flags["C_CONTIGUOUS"]    # True: the rows lie consecutively
index.T.flags["C_CONTIGUOUS"]  # False: the transpose is laid out otherwise
