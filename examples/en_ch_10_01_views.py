import numpy as np

index = np.zeros((1_000_000, 128), dtype=np.float32)

head = index[:1000]              # a view: no memory allocated
column = index[:, 7]             # a view with a 512-byte stride
picked = index[[3, 17, 999]]     # a copy: fancy indexing
sliced = index[3:20:2]           # a view: double the stride

head[0, 0] = 1.0
assert index[0, 0] == 1.0        # the original has changed
