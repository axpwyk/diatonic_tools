from theories import *

scale_name = 'C Harmonic Lydian'
scale = AlteredDiatonicScale(scale_name)
print(scale_name, ':', scale)
for i in range(7):
    ch = scale.get_full_chord(i)
    print(ch.get_name(), end='\n')
