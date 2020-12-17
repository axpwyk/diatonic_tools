import os; os.chdir('../..')
from theories import *

print(ChordEx().set_notes(bass=[Note('F')], notes=[Note('C'), Note('E'), Note('G'), Note('B')]).get_name())
print()

itv_1 = Interval('m3') + Interval('m3') + Interval('m3') + Interval('m3')
itv_2 = Interval('M3') + Interval('M3') + Interval('M3')
print(itv_1)
print(itv_2)
print()
