from theories import *


def get_7th_chord(scale, degree):
    l = len(scale.get_notes())
    degree = degree % l
    ret = []
    for i in range(4):
        idx = (degree+2*i)
        ret.append(scale[idx%l] if idx<l else scale[idx%l]+Interval('P8'))
    return ret


scale = AlteredDiatonicScale('E Phrygian(#3)')
print('E Phrygian(#3)', end='\t')
for i in range(7):
    ch = Chord().set_notes(body=get_7th_chord(scale, i))
    print(ch.get_name(), end='\t')

print()

scale = AlteredDiatonicScale('E Aeolian(#6, #7)')
print('E Aeolian(#6, #7)', end='\t')
for i in range(7):
    ch = Chord().set_notes(body=get_7th_chord(scale, i))
    print(ch.get_name(), end='\t')

print()

scale = AlteredDiatonicScale('C Lydian(b6)')
print('C Lydian(b6)', end='\t')
for i in range(7):
    ch = Chord().set_notes(body=get_7th_chord(scale, i))
    print(ch.get_name(), end='\t')

print()

print('AbM7+5: ', Chord('AbM7+5'))
print('Bm6: ', Chord('Bm6'))

print()

scale = AlteredDiatonicScale('C Ionian(#2)')
print('C Ionian(#5)', end='\t')
for i in range(7):
    ch = Chord().set_notes(body=get_7th_chord(scale, i))
    print(ch.get_name(), end='\t')
