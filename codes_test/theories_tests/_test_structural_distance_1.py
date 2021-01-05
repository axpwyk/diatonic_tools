import numpy as np
import matplotlib.pyplot as plt

def distance(scale_1, scale_2):
    a = np.expand_dims(np.array(scale_1), axis=-1)  # [M, 1]
    b = np.expand_dims(np.array(scale_2), axis=-1)  # [M, 1]
    x = np.expand_dims(np.arange(12), axis=0)  # [1, N]

    ax = np.expand_dims(np.sort((a + x) % 12, axis=0), axis=-1)  # [M, N, 1]
    bx = np.expand_dims(np.sort((b + x) % 12, axis=0), axis=-2)  # [M, 1, N]

    ds = np.sum((12 - np.abs(2 * np.abs(ax - bx) - 12)) // 2, axis=0)  # [N, N]

    return np.min(ds), np.where(ds == np.min(ds))


y_min = distance([0, 2, 4, 5, 7, 9, 11], [0, 2, 4, 6, 7, 9, 10])

print(f'y_min: {y_min}')
