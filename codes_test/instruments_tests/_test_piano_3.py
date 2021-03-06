import instruments as inst
from theories import *

root = Note('C')
itv1 = Interval('m2')
itv2 = Interval('M2')

notes = [root.set_message(br357t='R'),
         root+itv2,
         root+itv2+itv2,
         root+itv2+itv2+itv1,
         root+itv2+itv2+itv1+itv2,
         root+itv2+itv2+itv1+itv2+itv2,
         root+itv2+itv2+itv1+itv2+itv2+itv2,
         root+itv2+itv2+itv1+itv2+itv2+itv2+itv1]

inst.Piano(notes).plot_old(title=ChordEx().set_notes(notes=notes).get_name_old())

inst.plt.savefig('test_piano_plot.svg', bbox_inches='tight', pad_inches=0.0)
