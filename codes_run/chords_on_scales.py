from theories import *


def get_7th_chord(scale, degree):
    l = len(scale.get_notes())
    degree = degree % l
    ret = []
    for i in range(4):
        idx = (degree+2*i)
        ret.append(scale[idx%l] if idx<l else scale[idx%l]+Interval('P8'))
    return ret


scale = AlteredDiatonicScale('C Ionian(b6)')
print(scale)
print('A Aeolian(#7)', end='\t')
for i in range(7):
    ch = Chord().set_notes(body=get_7th_chord(scale, i))
    print(ch.get_name(), end='\t')
