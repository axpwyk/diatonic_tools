import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse
from matplotlib.transforms import ScaledTranslation
from matplotlib.font_manager import FontProperties

from midi import *
from movie import *


fps = 24
n_frames = 72
dpi = 300
resolution = (1280, 480)


plt.style.use('seaborn-pastel')

fig = plt.figure(figsize=(resolution[0]/dpi, resolution[1]/dpi), dpi=144)
ax = plt.gca(aspect='equal')
# ax.set_axis_off()
ax.set_xticks([])
ax.set_yticks([])
# ax.set_frame_on(False)
ax.set_xlim((-11.5, 11.5))
ax.set_ylim((-11.5, 11.5))

ell1 = Ellipse((-10,-10), 1, 1, 45, color=[0.75, 0.25, 0.75])
ell2 = Ellipse((-10, 10), 1, 1, -45, )
text = plt.text(0, 0, 'motion with acceleration', {'fontsize': 20, 'va': 'center', 'ha': 'center'})


def init():
    ax.add_patch(ell1)
    ax.add_patch(ell2)
    text.set_color([0, 0, 0])
    return ell1, ell2, text


def frame(i):
    pos1 = lambda t: fancy_motion(t, 0, n_frames, (-10, -10), (10, 10), type='slow-in-out', factor=5.0)
    pos2 = lambda t: fancy_motion(t, 0, n_frames, (-10, 10), (10, -10), type='fast-in-out', factor=5.0)
    if 0 <= i < n_frames/2:
        scale1 = lambda t: fancy_motion(t, 0, n_frames/2, 1, 3, type='slow-in-fast-out', factor=5.0)
        scale2 = lambda t: fancy_motion(t, 0, n_frames/2, 3, 1, type='fast-in-slow-out', factor=5.0)
    else:
        scale1 = lambda t: fancy_motion(t, n_frames/2, n_frames, 3, 1, type='fast-in-slow-out', factor=5.0)
        scale2 = lambda t: fancy_motion(t, n_frames/2, n_frames, 1, 3, type='slow-in-fast-out', factor=5.0)

    ell1.set_center(pos1(i)[0])
    ell1.width = scale1(i) * 1
    ell2.set_center(pos2(i)[0])
    ell2.width = scale2(i) * 1

    color = lambda t: fancy_motion(t, 0, n_frames, (1, 0, 1), (0.5, 1, 0.5), type='slow-in-out', factor=5.0)
    fontsize = lambda t: fancy_motion(t, 0, n_frames, 0, 72, type='slow-in-fast-out', factor=0.0)
    fontweight = lambda t: fancy_motion(t, 0, n_frames, 120, 2, type='slow-in-fast-out', factor=0.0)
    rotation = lambda t: fancy_motion(t, 0, n_frames, 30, 0, type='fast-in-slow-out', factor=0.0)
    family = lambda t: fancy_motion(t, 0, n_frames, 0, 10)

    text.set_color(*color(i))
    text.set_fontproperties(FontProperties(size=fontsize(i)[0, 0], weight=fontweight(i)[0, 0]))
    text.set_rotation(rotation(i)[0, 0])
    text.set_fontfamily(['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'][int(family(i)[0, 0])%5])

    print(f'current frame: {i} | ell1.width: {ell1.width}')
    return ell1, ell2, text


anim = FuncAnimation(fig, frame, init_func=init, frames=n_frames, blit=True)
anim.save('transform_test2.gif', writer='imagemagick', codec='png', savefig_kwargs={'transparent': True, 'facecolor': None}, fps=fps)
# anim.save('transform_test.mov', codec='png', savefig_kwargs={'transparent': True, 'facecolor': None}, fps=fps)
