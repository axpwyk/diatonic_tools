import os; os.chdir('../..')
from theories import *
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-pastel')
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})


with open('__old__/all_heptatonic_scale_classes.txt', 'r') as f:
    classes = []
    for line in f:
        classes.append(eval(line)[0])


# calculate distance matrix
distances = np.zeros((66, 66), np.int)

for i in range(len(classes)):
    notes_i = AlteredDiatonicScale('C '+classes[i])
    for j in range(len(classes)):
        notes_j = AlteredDiatonicScale('B# '+classes[j])
        d = notes_i.distance_1(notes_j)
        distances[i, j] = d

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

# plot distance matrix
plt.imshow(distances)
plt.show()
