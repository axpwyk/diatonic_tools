import os; os.chdir('../..')
from theories import *
import numpy as np
import matplotlib.pyplot as plt


plt.style.use('seaborn-pastel')
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})


def d1(x, y):
    return min(abs(x-y), 12-abs(x-y))


def dn(xs, ys):
    ds = []
    for i in range(len(xs)):
        tmp = []
        for x, y in zip(np.roll(xs, i), ys):
            tmp.append(d1(x, y))
        ds.append(sum(tmp))
    return min(ds)


def d(xs, ys):
    ds = []
    for k in np.arange(12):
        ds.append(dn(np.mod(xs+k, 12), ys))
    return min(ds), ds


with open('all_heptatonic_scale_classes.txt', 'r') as f:
    classes = []
    for line in f:
        classes.append(eval(line)[0])


# calculate distance matrix
distances = np.zeros((66, 66), np.int)
for i in range(len(classes)):
    notes_i = AlteredDiatonicScale('C '+classes[i]).get_nnabs_list()
    notes_i = [n%12 for n in notes_i]  # this algorithm do not support negative note number
    for j in range(len(classes)):
        notes_j = AlteredDiatonicScale('C '+classes[j]).get_nnabs_list()
        notes_j = [n%12 for n in notes_j]  # this algorithm do not support negative note number
        distances[i, j] = d(notes_i, notes_j)[0]
        # if i in [0, 65] and j in [0, 65] and i != j:
        #     print(classes[i], classes[j])
        #     print(notes_i)
        #     print(notes_j)
        #     print(f'({i}, {j}):', d(notes_i, notes_j)[1])
print(np.where(distances.transpose()!=distances))


# triangle ineq.
dist_tensor = np.zeros((66, 66, 66), np.bool)

for i in range(66):
    for j in range(66):
        for k in range(66):
            dist_tensor[i, j, k] = (distances[i, j] + distances[j, k] >= distances[i, k]) and \
                                   (distances[j, k] + distances[k, i] >= distances[j, i]) and \
                                   (distances[k, i] + distances[i, j] >= distances[k, j])
print(np.where(dist_tensor==False))

print(distances)
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
