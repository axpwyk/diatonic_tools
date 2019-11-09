import matplotlib.pyplot as plt
import matplotlib.transforms as mt

fig = plt.figure(figsize=(5, 5), dpi=144)
fig.subplots_adjust(right=1.0, left=0.0, bottom=0.0, top=1.0, wspace=0.1, hspace=0.1)
ax = plt.gca()
ax.set_axis_off()
ax.axis('equal')
ax.margins(x=0, y=0)

rect = plt.Rectangle((0, 0), 1, 1, fc='#ccddee', ec='#000000')
ax = plt.gca()
ax.add_patch(rect)
plot = ax.plot((-1, 2, 0.5, 0.5, -1), (0.5, 0.5, 1, 0, 0.5), marker='x', markersize=10)
print(plot)
plot[0].set_clip_path(rect)

plt.savefig(r'../output/mpl_clip.svg')
plt.show()
