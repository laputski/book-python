import numpy as np

index = np.zeros((1_000_000, 128), dtype=np.float32)

head = index[:1000]              # представление: памяти не выделено
column = index[:, 7]             # представление с шагом 512 байт
picked = index[[3, 17, 999]]     # копия: выборка по списку индексов
sliced = index[3:20:2]           # представление: шаг вдвое больше

head[0, 0] = 1.0
assert index[0, 0] == 1.0        # исходный массив изменён
