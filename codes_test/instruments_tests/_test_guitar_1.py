import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-pastel')

w_scale = 2
strings = np.array([0, 1, 2, 3, 4, 5])
fret = w_scale * np.arange(0, 24)
fingers = np.concatenate([[-0.5], fret[:-1]+fret[1:]]) / 2

# new figure
fig = plt.figure(figsize=(5, 4), dpi=72)
ax = plt.gca(aspect='equal')
ax.set_xticks([]); ax.set_yticks([])
ax.set_axis_off()
ax.margins(0.0)

# plot strings
ax.set_ylim(strings[0]-1, strings[-1]+1)
_ = [ax.plot_old((0, fret[4]), (s, s), c='black', lw=1.0) for s in strings]

# plot frets
ax.set_xlim(fret[0]-1, fret[4]+2.5)
_ = [ax.plot_old((fret[i], fret[i]), (0, strings[-1]), c='black', lw=2.0) for i in range(5)]
_ = [ax.annotate(fret[i]//w_scale, (fret[i], -0.3), color='blue', va='center', ha='center', bbox=dict(facecolor='blue', alpha=0.2)) for i in range(5)]

# plot dots
circs = []
circs.append(plt.Circle((fingers[0], strings[0]), 0.15, fc='white', ec='black'))
circs.append(plt.Circle((fingers[2], strings[1]), 0.15, fc='black', ec='black'))
circs.append(plt.Circle((fingers[2], strings[2]), 0.15, fc='black', ec='black'))
circs.append(plt.Circle((fingers[0], strings[3]), 0.15, fc='white', ec='black'))
circs.append(plt.Circle((fingers[0], strings[4]), 0.15, fc='white', ec='black'))
circs.append(plt.Circle((fingers[0], strings[5]), 0.15, fc='white', ec='black'))
_ = [ax.add_patch(circ) for circ in circs]

# add string text
texts1 = ['E1', 'B1', 'E2', 'G2', 'B2', 'E3']
_ = [ax.annotate(text, (fret[4]+w_scale*0.25, strings[i]), va='center', ha='left', bbox=dict(facecolor='red', alpha=0.2)) for i, text in enumerate(texts1)]
texts2 = ['R', '5', 'R', '3', '5', 'R']
_ = [ax.annotate(text, (fret[4]+w_scale*0.75, strings[i]), va='center', ha='left', bbox=dict(facecolor='orange', alpha=0.2)) for i, text in enumerate(texts2)]

fig.savefig('三个和弦的键盘示意图.svg', bbox_inches='tight', pad_inches=0.0)
