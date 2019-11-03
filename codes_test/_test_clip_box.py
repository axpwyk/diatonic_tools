import matplotlib.pyplot as plt
from matplotlib.transforms import TransformedBbox

ax = plt.gca()
rect = plt.Rectangle((0.4, 0.4), 0.28, 0.3, lw=0.0, )
# text = plt.Text(0.5, 0.5, 'abcdefghijklmnopqrstuvwxyz', clip_box=rect.get_bbox().transformed(ax.transData))
ax.add_patch(rect)
# ax.add_artist(text)
plt.annotate('abcdefghijklmnopqrstuvwxyz', (0.5, 0.5), clip_box=TransformedBbox(rect.get_bbox(), ax.transData))
plt.text(0.4, 0.4, 'abcdefghijklmnopqrstuvwxyz', clip_box=TransformedBbox(rect.get_bbox(), ax.transData))
plt.savefig(r'../output/text_clip.svg')
