import numpy as np

index = np.zeros((1_000_000, 128), dtype=np.float32)   # построчный порядок

index[42]          # 128 чисел подряд: одно обращение к участку памяти
index[:, 42]       # 1 000 000 чисел с шагом 512 байт: обращение на каждое

index.flags["C_CONTIGUOUS"]    # True: строки лежат подряд
index.T.flags["C_CONTIGUOUS"]  # False: у транспонированного порядок иной
