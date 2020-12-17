import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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


''' ======================================================= '''
''' 2d landscape                                            '''
''' ======================================================= '''


# p = 96
# xy = np.stack(np.meshgrid(np.linspace(0, 12, p), np.linspace(0, 12, p)), axis=-1)
# z = np.zeros((p, p))
# for i in range(p):
#     for j in range(p):
#         z[i, j] = d(xy[i, j, 0], xy[i, j, 1])
#
# ax = plt.gca(projection='3d')
# ax.contour(xy[:, :, 0], xy[:, :, 1], z, color=[1.0, 0.5, 0.0])
# plt.show()


''' ======================================================= '''
''' Heptatonic Scales                                       '''
''' ======================================================= '''


# xs = np.array([0, 2, 4, 5, 7, 9, 11])  # C Ionian
# ys = np.array([9, 10, 0, 2, 4, 6, 7])  # A Dorian(b2)

# xs = np.array([5, 8, 10, 11, 0, 2, 4])  # Lydian(#2, #3)
# ys = np.array([5, 7, 9, 11, 1, 3, 4])  # Lydian(#5, #6)

# xs = np.array([5, 8, 9, 11, 0, 2, 3])  # Lydian(#2, b7)
# ys = np.array([5, 7, 9, 11, 0, 2, 4])  # Lydian

xs = np.array([0, 2, 4, 5, 7, 9, 11])
ys = np.array([0, 1, 2, 3, 4, 5, 6])

ds = []
for k in np.linspace(0, 12, 1200):
    ds.append(dn(np.mod(xs+k, 12), ys))

plt.grid(zorder=-1)
plt.plot(ds, zorder=9)
plt.scatter(np.linspace(0, 1200, 12, False), np.round(ds[::100]), 50, 'red', zorder=10)
plt.show()
