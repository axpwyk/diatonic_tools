# THIS DISTANCE ALGORITHM IS NOT RIGHT
# [3] 1 2 [1] 2 1 2 (Lydian(#2, b7))
# [2] 1 2 [2] 2 1 2 (Dorian)
from theories import *
import numpy as np
import matplotlib.pyplot as plt


plt.style.use('seaborn-pastel')
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})


# THIS DISTANCE ALGORITHM IS NOT RIGHT
def d(notes_1, notes_2):
    def _lshift(lst, k):
        return lst[k:] + lst[:k]

    def _dist(lst1, lst2):
        return sum([abs(e2-e1) for e1, e2 in zip(lst1, lst2)])/2

    intervals_1 = [(n1-n2)%12 for n1, n2 in zip(_lshift(notes_1, 1), notes_1)]
    intervals_2 = [(n1-n2)%12 for n1, n2 in zip(_lshift(notes_2, 1), notes_2)]

    ds = []
    for k in range(12):
        ds.append(_dist(_lshift(intervals_1, k), intervals_2))

    return min(ds)


with open('../all_heptatonic_scale_classes.txt', 'r') as f:
    classes = []
    for line in f:
        classes.append(eval(line)[0])


# calculate distance matrix
distances = np.zeros((66, 66), np.int)
for i in range(len(classes)):
    notes_i = abs(AlteredDiatonicScale('C '+classes[i]))
    for j in range(len(classes)):
        notes_j = abs(AlteredDiatonicScale('C '+classes[j]))
        distances[i, j] = d(notes_i, notes_j)

print(np.any(distances.transpose()!=distances))

# triangle ineq.
dist_tensor = np.zeros((66, 66, 66), np.bool)

for i in range(66):
    for j in range(66):
        for k in range(66):
            dist_tensor[i, j, k] = (distances[i, j] + distances[j, k] >= distances[i, k]) and \
                                   (distances[j, k] + distances[k, i] >= distances[j, i]) and \
                                   (distances[k, i] + distances[i, j] >= distances[k, j])

print(np.any(dist_tensor==False))

plt.imshow(distances)
plt.show()
