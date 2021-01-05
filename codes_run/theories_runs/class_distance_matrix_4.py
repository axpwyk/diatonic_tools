import os; os.chdir('../..')
from theories import *
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-pastel')
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})


def distance(scale_a, scale_b):
    a = np.expand_dims(np.array(scale_a.get_nnabs_list()), axis=-1)  # [M, 1]
    b = np.expand_dims(np.array(scale_b.get_nnabs_list()), axis=-1)  # [M, 1]
    x = np.expand_dims(np.arange(N), axis=0)  # [1, N]

    ax = np.expand_dims(np.sort((a + x) % N, axis=0), axis=-1)  # [M, N, 1]
    bx = np.expand_dims(np.sort((b + x) % N, axis=0), axis=-2)  # [M, 1, N]

    ds = np.sum((N - np.abs(2 * np.abs(ax - bx) - N)) // 2, axis=0)  # [N, N]
    d = np.min(ds)

    offsets_ab = np.stack(np.where(ds == d), axis=-1)
    offsets_ab = offsets_ab[np.any(offsets_ab == 0, axis=1)]  # rotations of a and b (counterclockwise)

    return d, offsets_ab


with open('all_heptatonic_scale_classes.txt', 'r') as f:
    classes = []
    for line in f:
        classes.append(eval(line)[0])


# calculate distance matrix
distances = np.zeros((66, 66), np.int)
offsets_ab = dict()

for i in range(len(classes)):
    notes_i = AlteredDiatonicScale('C '+classes[i])
    for j in range(len(classes)):
        notes_j = AlteredDiatonicScale('C '+classes[j])
        d, oab = distance(notes_i, notes_j)
        distances[i, j] = d
        offsets_ab[f'{66 * i + j}'] = oab

# check symmetry
for c1, c2 in zip(*np.where(distances.transpose()!=distances)):
    print(c1, c2, classes[c1], classes[c2])

# check triangle inequalities
dist_tensor = np.zeros((66, 66, 66), np.bool)
for i in range(66):
    for j in range(66):
        for k in range(66):
            dist_tensor[i, j, k] = (distances[i, j] + distances[j, k] >= distances[i, k]) and \
                                   (distances[j, k] + distances[k, i] >= distances[j, i]) and \
                                   (distances[k, i] + distances[i, j] >= distances[k, j])

for c1, c2, c3 in zip(*np.where(dist_tensor==False)):
    print(c1, c2, c3, classes[c1], classes[c2], classes[c3])

# print offsets_ab
for key, value in offsets_ab.items():
    i = int(key) // 66
    j = int(key) % 66
    if i == 0 and j == 17:
        print(f'{i} -> {j}: {value}')

# plot distance matrix
plt.imshow(distances)
plt.show()
