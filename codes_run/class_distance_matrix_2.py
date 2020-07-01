from theories import *
import numpy as np
import matplotlib.pyplot as plt

# scale1 = abs(AlteredDiatonicScale('C Lydian(#3,#6)'))
# scale2 = abs(AlteredDiatonicScale('C Lydian(b6,b7)'))
# scale1 = [0,1,2,3,4,5,6]
# scale2 = [9,0,1,2,4,5,6]
# scale1 = abs(AlteredDiatonicScale('C Lydian(#2,#3)'))
# scale2 = abs(AlteredDiatonicScale('C Lydian(#5,#6)'))


def d(notes_1, notes_2):
    def _lshift(lst, k):
        return lst[k:] + lst[:k]

    def _moves(hot1, hot2):
        n = len(hot1)
        moves = 0
        for k in range(n):
            if hot1[k] == hot2[k]: continue
            elif not hot1[k]:
                if True in hot1[k:]:
                    idx = hot1[k:].index(True)
                    hot1[k] = not hot1[k]
                    hot1[k+idx] = not hot1[k+idx]
                    moves += idx
            elif not hot2[k]:
                if True in hot2[k:]:
                    idx = hot2[k:].index(True)
                    hot2[k] = not hot2[k]
                    hot2[k+idx] = not hot2[k+idx]
                    moves += idx
        return moves

    notes_1_hot = [True if k in [note%12 for note in notes_1] else False for k in range(12)]
    notes_2_hot = [True if k in [note%12 for note in notes_2] else False for k in range(12)]

    ds = []
    for i in range(12):
        for j in range(12):
            ds.append(_moves(_lshift(notes_1_hot, i), _lshift(notes_2_hot, j)))

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

plt.imshow(distances)
plt.show()
