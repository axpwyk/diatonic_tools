import os; os.chdir('../..')
from theories import *
import numpy as np
import matplotlib.pyplot as plt


plt.style.use('seaborn-pastel')
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})


def d(notes_1, notes_2):
    def _lshift(lst, k):
        return lst[k:] + lst[:k]

    def _dist(lst1, lst2):
        return sum([abs(e2-e1) for e1, e2 in zip(lst1, lst2)])

    notes_1_hot = [1 if k in [note%12 for note in notes_1] else 0 for k in range(12)]
    notes_2_hot = [1 if k in [note%12 for note in notes_2] else 0 for k in range(12)]

    ds = []
    for k in range(12):
        for t in range(12):
            notes_1_hot_rotated = _lshift(notes_1_hot, k)
            notes_1_hot_rotated = _lshift(notes_1_hot_rotated, t)
            notes_2_hot_rotated = _lshift(notes_2_hot, t)
            notes_1_rotated = [i for i, j in enumerate(notes_1_hot_rotated) if j!=0]
            notes_2_rotated = [i for i, j in enumerate(notes_2_hot_rotated) if j!=0]
            ds.append(_dist(notes_1_rotated, notes_2_rotated))

    return min(ds)


with open('all_heptatonic_scale_classes.txt', 'r') as f:
    classes = []
    for line in f:
        classes.append(eval(line)[0])


# calculate distance matrix
distances = np.zeros((66, 66), np.int)
for i in range(len(classes)):
    notes_i = AlteredDiatonicScale('C '+classes[i]).get_nnabs_list()
    for j in range(len(classes)):
        notes_j = AlteredDiatonicScale('C '+classes[j]).get_nnabs_list()
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


# plot
# distances = np.pad(distances, ((1, 1), (1, 1)), 'constant')
#
# fig = plt.figure(None, (10, 10), 300)
# ax = plt.gca()
# ax.set_axis_off()
# ax.set_frame_on(False)
# ax.margins(0.0)
# ax.imshow(distances, cmap='gray')
# for i in range(66):
#     for j in range(66):
#         ax.text(j+1, i+1, distances[i+1, j+1], fontsize=5,
#                        ha='center', va='center', color='w')
# for i in range(1, 67):
#     ax.text(0, i, i-1, fontsize=5, ha='center', va='center', color='w')
#     ax.text(67, i, i-1, fontsize=5, ha='center', va='center', color='w')
#     ax.text(i, 0, i-1, fontsize=5, ha='center', va='center', color='w')
#     ax.text(i, 67, i-1, fontsize=5, ha='center', va='center', color='w')
#
# fig.savefig('三个和弦的键盘示意图.svg', fc='none', bbox_inches='tight', pad_inches=0.0, dpi=300)
