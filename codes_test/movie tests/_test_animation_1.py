import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

n_frames = 120
frame_rate = 120

plt.style.use('seaborn-pastel')

fig = plt.figure(figsize=(4, 3), dpi=144)
ax = plt.gca(aspect='equal')
ax.set_axis_off()
ax.set_xlim((-3, 3))
ax.set_ylim((-3, 3))

grid = np.reshape(np.stack(np.meshgrid(np.linspace(-3, 2, 6), np.linspace(-3, 2, 6)), axis=-1), (-1, 2))
print(grid)
rects = [plt.Rectangle(xy, 1.0, 1.0, 0.0, lw=0.0) for xy in grid]


def init():
    _ = [ax.add_patch(rect) for rect in rects]
    return rects


def frame(i):
    _ = [rect.set_color([((i+j)/len(rects))%1.00]*3) for j, rect in enumerate(rects)]
    return rects


anim = FuncAnimation(fig, frame, init_func=init, frames=n_frames, blit=True)
anim.save('test.mov', codec='png', dpi=144, bitrate=-1, savefig_kwargs={'transparent': True, 'facecolor': None}, fps=60)
