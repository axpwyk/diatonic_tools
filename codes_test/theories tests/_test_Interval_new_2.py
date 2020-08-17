import os; os.chdir('../..')
from theories import *

print(ChordEx().set_notes(bass=[Note('F')], notes=[Note('C'), Note('E'), Note('G'), Note('B')]).get_name())
print()

print(Interval('dd1')+Interval('-P4'))
print()
