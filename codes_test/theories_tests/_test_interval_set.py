import os; os.chdir('../../codes_run')
from theories import *

# notes1 = AlteredDiatonicScale('C Ionian(b3)')
# notes2 = AlteredDiatonicScale('D Aeolian(#3)')

notes1 = Chord('C')
notes2 = Chord('C7(#9)')

itvs1 = [a - b for a in notes1 for b in notes1]
itvs1 = [itv.normalize().get_name_old() for itv in itvs1]
itvs1 = set(itvs1)

itvs2 = [a - b for a in notes2 for b in notes2]
itvs2 = [itv.normalize().get_vector()[0] for itv in itvs2]
itvs2 = set(itvs2)

print(itvs1, '\n', itvs2)
