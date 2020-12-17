from theories import *

scale_names = ['F Lydian', 'F Lydian(#2)', 'F Lydian(#3)', 'F Lydian(#5)', 'F Lydian(#6)', 'F Lydian(b2)', 'F Lydian(b3)', 'F Lydian(b6)', 'F Lydian(#2, #6)', 'F Lydian(#5, #6)']


def show_chords(scale_name):
    scale = AlteredDiatonicScale(scale_name)
    print(scale_name, ':', scale)
    for i in range(7):
        ch = scale.get_full_chord(i)
        print(ch.get_name(), end='\t')
    print('\n')


for scale_name in scale_names:
    show_chords(scale_name)
