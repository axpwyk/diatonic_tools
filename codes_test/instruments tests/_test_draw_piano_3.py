import instruments as inst
from theories import *

root = Note('C')
itv1 = Interval('m2')
itv2 = Interval('M2')

notes = [root.set_message('R'),
         root+itv2,
         root+itv2+itv2,
         root+itv2+itv2+itv1,
         root+itv2+itv2+itv1+itv2,
         root+itv2+itv2+itv1+itv2+itv2,
         root+itv2+itv2+itv1+itv2+itv2+itv2,
         root+itv2+itv2+itv1+itv2+itv2+itv2+itv1]

inst.Piano(notes).plot(title=ChordEx().set_notes(notes=notes).get_name())

inst.plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
