from theories import *

print(Chord('Abm').get_icd('Dbb'))
print(Chord('GbM7(9, #11)').get_scale()[0].set_scale_tonic_str('C').get_name_old())
print(AlteredDiatonicScale('B Aeolian(#1)'))
