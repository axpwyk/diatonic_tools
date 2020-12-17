import itertools
import numpy as np
import matplotlib.pyplot as plt


def moves(hot1, hot2):
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


print(moves([1,1,1,1,1,1,1,0,0,0,0,0], [1,1,1,0,1,1,1,0,0,1,0,0]))


def d(notes_1_hot, notes_2_hot):
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

    ds = []
    for i in range(12):
        for j in range(12):
            ds.append(_moves(_lshift(notes_1_hot, i), _lshift(notes_2_hot, j)))

    return min(ds)


distances = np.zeros((512, 512), np.int)
for i, j in itertools.combinations(range(512), 2):
    distances[i, j] = d([eval(x) for x in bin(i)[2:]], [eval(x) for x in bin(j)[2:]])
    distances[j, i] = distances[i, j]

plt.imshow(distances)
plt.show()
