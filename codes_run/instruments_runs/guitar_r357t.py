from instruments import *

g = GuitarV2().set_notes(Chord('D maj7(b2, 2, b3, 4, #4, b6, 6, b7)'))
g.plot(0, 16, color_style='br357t', text_rotation=-5)
plt.savefig('guitar_r357t.svg', dpi=144, bbox_inches='tight')
