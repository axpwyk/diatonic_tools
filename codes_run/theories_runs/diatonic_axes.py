import matplotlib.pyplot as plt
import numpy as np


# assign a style
plt.style.use('seaborn-pastel')
# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})
# assign a chinese font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})
plt.rc('axes', **{'unicode_minus': False})


fig = plt.figure(figsize=(5, 4), dpi=144)
ax = plt.gca(aspect='equal')
t = np.arange(0, 13, dtype='int')
tonics = [r'A$\flat$', r'E$\flat$', r'B$\flat$', 'F', 'C', 'G',
          'D',
          'A', 'E', 'B', r'F$\sharp$', r'C$\sharp$', r'G$\sharp$']
modes = [r'$\flat$ Mixolydian', r'$\flat$ Ionian', r'$\flat$ Lydian', 'Locrian', 'Phrygian', 'Aeolian',
         'Dorian',
         'Mixolydian', 'Ionian', 'Lydian', r'$\sharp$ Locrian', r'$\sharp$ Phrygian', r'$\sharp$ Aeolian']
chord_types = [r'$\flat$7', r'$\flat$M7', r'$\flat$M7', 'm7-5', 'm7', 'm7',
               'm7',
               '7', 'M7', 'M7', r'$\sharp$m7-5', r'$\sharp$m7', r'$\sharp$m7']
print(t)
print(tonics)
print(modes)

# 坐标系设置
ax.set_xlim(t.min(), t.max())
ax.set_ylim(t.min(), t.max())
ax.set_xticks(t); ax.set_xticklabels(tonics)
ax.set_yticks(t); ax.set_yticklabels(modes)
ax.grid()
left = t.min()
right = t.max()
mid = (right-left)//2
ax.plot_old([left, right], [mid, mid], 'r', linewidth=1, zorder=2)
ax.plot_old([mid, mid], [left, right], 'r', linewidth=1, zorder=2)

# 等升降号线
ax.plot_old([0, right], [right, 0], 'blue', linewidth=1, linestyle=':', alpha=0.5, zorder=3)
for k in range(1, right):
    ax.plot_old([k, right], [right, k], 'blue', linewidth=1, linestyle=':', alpha=0.5, zorder=3)
    ax.plot_old([0, right - k], [right - k, 0], 'blue', linewidth=1, linestyle=':', alpha=0.5, zorder=3)

# 升降号个数
for k in t[1:-1]:
    ax.annotate((k-mid)*2, (k, k), ha='center', va='center',
                bbox=dict(facecolor='blue', alpha=0.2, edgecolor='blue'))

# 和弦类型
for k in range(right+1):
    ax.annotate(chord_types[k], (right+0.5, k), ha='left', va='center', annotation_clip=False)

# 标题
# ax.set_title('Diatonic Modes & Chords Cheat Sheet by ykykyukai\n', ha='center')

# savefig('diatonic_cheat_sheet_v2.svg')
fig.show()
