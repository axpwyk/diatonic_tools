import instruments as inst
from theories import *

root = Note('C')
itv = Interval('-d1')
notes = [root, root+itv, root+itv+itv, root+itv+itv+itv, root+itv+itv+itv+itv]
inst.Piano(notes).plot(title='连续的负减一度叠置')

inst.plt.savefig('test_piano_plot.svg', bbox_inches='tight', pad_inches=0.0)
