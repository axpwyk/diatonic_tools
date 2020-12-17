from theories import *

print(Chord('Abm').get_icd('Dbb'))
print(Chord('GbM7(9, #11)').get_scale()[0].set_tonic('C').get_name())
print(AlteredDiatonicScale('B Aeolian(#1)'))
