import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.animation import FuncAnimation

from midi import *


sheet, ticks_per_beat, _ = midi2sheet('../../midi/nvdrums.mid')
pr = Pianoroll(sheet, ticks_per_beat)

fps = 60

kick_ons, kick_offs, kick_vels = pr.get_key_frames(track=1, note=36, bpm=164, fps=fps)
kick_n_frames = max(kick_offs)
snare_normal_ons, snare_normal_offs, snare_normal_vels = pr.get_key_frames(track=1, note=38, bpm=164, fps=fps)
snare_normal_n_frames = max(snare_normal_offs)
snare_rimshot_ons, snare_rimshot_offs, snare_rimshot_vels = pr.get_key_frames(track=1, note=37, bpm=164, fps=fps)
snare_rimshot_n_frames = max(snare_rimshot_offs)

n_frames = max(kick_n_frames, snare_normal_n_frames, snare_rimshot_n_frames)


plt.style.use('seaborn-pastel')

fig = plt.figure(figsize=(512/144, 512/144), dpi=144)
ax = plt.gca(aspect='equal')
ax.set_axis_off()
ax.set_frame_on(False)
ax.set_xlim((-3, 3))
ax.set_ylim((-3, 3))

kick = plt.Circle((-1, 0), 0, facecolor=[0.0, 0.0, 0.0], zorder=10, hatch=r'//')
snare_normal = plt.Circle((1, 0), 0, facecolor=[0.0, 0.0, 0.0], hatch=r'\\')
snare_rimshot = plt.Circle((1, 0), 0, facecolor=[0.0, 0.0, 0.0], hatch=r'\\')


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
        k = 16
        return (np.exp(k*ts)-1)/(np.exp(k)-1)
    return np.clip((pos2-pos1)*(g((ts-time1)/(time2-time1))-g(0))+pos1, min(pos1, pos2), max(pos1, pos2))


def init():
    ax.add_patch(kick)
    ax.add_patch(snare_normal)
    ax.add_patch(snare_rimshot)
    return kick, snare_normal, snare_rimshot


class Frame(object):
    def __init__(self):
        self.k1 = 0
        self.k2 = 0
        self.k3 = 0
        self.status1 = 'const'
        self.status2 = 'const'
        self.status3 = 'const'

    def __call__(self, i):
        if i == int(kick_ons[self.k1+1]):
            self.status1 = 'interp'
            self.k1 = self.k1 + 1
        if i == int(kick_offs[self.k1]):
            self.status1 = 'const'
        if i == int(snare_normal_ons[self.k2+1]):
            self.status2 = 'interp'
            self.k2 = self.k2 + 1
        if i == int(snare_normal_offs[self.k2]):
            self.status2 = 'const'
        if i == int(snare_rimshot_ons[self.k3+1]):
            self.status3 = 'interp'
            self.k3 = self.k3 + 1
        if i == int(snare_rimshot_offs[self.k3]):
            self.status3 = 'const'

        if self.status1 == 'interp':
            kick.set_radius(interp(i, kick_ons[self.k1], kick_offs[self.k1], kick_vels[self.k1]/127*1.5, 0))
            kick.set_color([interp(i, kick_ons[self.k1], kick_offs[self.k1], kick_vels[self.k1]/127, 0)[0, 0], 0, 0])
            kick.set_center((-1, interp(i, kick_ons[self.k1], kick_offs[self.k1], kick_vels[self.k1]/127*1, 0)))
        if self.status2 == 'interp':
            snare_normal.set_radius(interp(i, snare_normal_ons[self.k2], snare_normal_offs[self.k2], snare_normal_vels[self.k2]/127*1.5, 0))
            snare_normal.set_color([0, 0, interp(i, kick_ons[self.k1], kick_offs[self.k1], kick_vels[self.k1]/127, 0)[0, 0]])
            snare_normal.set_center((-1, interp(i, snare_normal_ons[self.k2], snare_normal_offs[self.k2], snare_normal_vels[self.k2]/127*1, 0)))
        if self.status3 == 'interp':
            snare_rimshot.set_radius(interp(i, snare_rimshot_ons[self.k3], snare_rimshot_offs[self.k3], snare_rimshot_vels[self.k3]/127*1.5, 0))
            snare_rimshot.set_color([0, 0, interp(i, kick_ons[self.k1], kick_offs[self.k1], kick_vels[self.k1]/127, 0)[0, 0]])
            snare_rimshot.set_center((-1, interp(i, snare_rimshot_ons[self.k3], snare_rimshot_offs[self.k3], snare_rimshot_vels[self.k3]/127*1, 0)))

        if i % 1000 == 0:
            print(f'frame {i}: {snare_rimshot.radius}')

        return kick, snare_normal, snare_rimshot


frame = Frame()
anim = FuncAnimation(fig, frame, init_func=init, frames=n_frames, blit=True)
anim.save('test.mov', codec='png', savefig_kwargs={'transparent': True, 'facecolor': None}, fps=fps)
