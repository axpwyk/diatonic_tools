import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.animation import FuncAnimation

n_frames = 120
fps = 60

plt.style.use('seaborn-pastel')

fig = plt.figure(figsize=(1920/144, 1080/144), dpi=144)
ax = plt.gca(aspect='equal')
ax.set_axis_off()
ax.set_frame_on(False)
ax.set_xlim((-3, 3))
ax.set_ylim((-3, 3))

circle = plt.Circle((-3, -3), 0.5, facecolor=[0.75, 0.5, 0.0])


def bezier3(lambdas, position_1, position_2, control_point_1, control_point_2):
    x0 = np.array(position_1).reshape((1, -1))
    x1 = np.array(control_point_1).reshape((1, -1))
    x2 = np.array(control_point_2).reshape((1, -1))
    x3 = np.array(position_2).reshape((1, -1))
    lambdas = np.reshape(np.array(lambdas), (-1, 1))
    return (1-lambdas)**3*x0 + 3*(1-lambdas)**2*lambdas*x1 + 3*(1-lambdas)*lambdas**2*x2 + lambdas**3*x3


def interp(ts, time1, time2, pos1, pos2):
    ts = np.array(ts).reshape((-1, 1))
    pos1 = np.array(pos1).reshape((1, -1))
    pos2 = np.array(pos2).reshape((1, -1))
    def g(ts):
        return (np.exp(5*ts)-1)/(np.exp(5)-1)
    return (pos2-pos1)*(g((ts-time1)/(time2-time1))-g(0))+pos1


def init():
    ax.add_patch(circle)
    return circle,


def frame(i):
    circle.set_center(interp(i, 0, 120, (-3, -3), (3, 3))[0])
    circle.set_radius(2-i/60)
    return circle,


anim = FuncAnimation(fig, frame, init_func=init, frames=n_frames, blit=True)
anim.save('test.mov', codec='png', savefig_kwargs={'transparent': True, 'facecolor': None}, fps=fps)
