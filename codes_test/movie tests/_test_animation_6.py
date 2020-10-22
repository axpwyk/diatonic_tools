import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse
from matplotlib.transforms import ScaledTranslation
from matplotlib.font_manager import FontProperties

from movie import *


fps = 60
n_frames = 300
dpi = 300
resolution = (256, 128)


plt.style.use('seaborn-pastel')

fig = plt.figure(figsize=(resolution[0]/dpi, resolution[1]/dpi), dpi=dpi)
plt.subplots_adjust(0.1, 0.1, 0.9, 0.9)
ax = plt.gca(aspect='equal')
ax.set_xticks([])
ax.set_yticks([])

n = 9
# t = np.linspace(-1.5*np.pi, 2.5*np.pi, n)
# x = 2*np.cos(t)
# y = 2*np.sin(t)
x = [0, 1, 1, 0, 0, 0, -1, -1, 0]
y = [0, 0, 1, 1, 0, -1, -1, 0, 0]
R = np.array([[np.cos(np.deg2rad(30)), -np.sin(np.deg2rad(30))], [np.sin(np.deg2rad(30)), np.cos(np.deg2rad(30))]])
xy = np.stack([x, y], axis=-1)
xy = np.dot(xy, R)
bc = Bezier(np.linspace(0, 1, 12000), xy)

lines = [plt.plot(*bc.get_control_points(k, 0), solid_capstyle='round', zorder=0, lw=0.5)[0] for k in range(n)]
curve = plt.plot(*bc.get_data(), color='red', solid_capstyle='round', zorder=1, lw=0.5)
circ = plt.Circle(bc.get_control_points(n-1, 0), 0.02, facecolor='red', zorder=2)
ax.add_patch(circ)


def init():
    return lines + [circ]


def frame(i):
    lbd = fancy_motion(i, 0, n_frames, 0, 12000, 'slow-in-out', 3.0)
    _ = [line.set_data(*bc.get_control_points(k, int(lbd))) for k, line in enumerate(lines)]
    curve[0].set_data(*bc.get_data()[:, :int(lbd)])
    circ.set_center(bc.get_control_points(n-1, int(lbd)))
    return lines + [circ]


anim = FuncAnimation(fig, frame, init_func=init, frames=n_frames, blit=True)
anim.save('../../output/matplotlib/export.gif', writer='imagemagick', codec='png', savefig_kwargs={'transparent': True, 'facecolor': None}, fps=fps)
# anim.save('../../output/matplotlib/export.mov', codec='png', savefig_kwargs={'transparent': True, 'facecolor': None}, fps=fps)
