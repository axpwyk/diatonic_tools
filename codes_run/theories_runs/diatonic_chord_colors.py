from theories import *

ds = DiatonicScale('C Mixolydian')
chords = []
for i in range(7):
    n = 2
    T = ds.get_chord(0, n)
    ch = Chord().set_notes(body=ds.get_chord(i, n))
    chords.append((ch.get_name(), '\t', get_color(ch) - get_color(T)))

for ch in sorted(chords, key=lambda x: x[2]):
    print(*ch)

# print(get_absolute_color([Note('F'), Note('C'), Note('G')]) - get_absolute_color([Note('A'), Note('E'), Note('B')]))
# print(get_absolute_color(Chord('E')) - get_absolute_color(Chord('Fm')))
# print(get_absolute_color(Chord('B')) - get_absolute_color(Chord('Am')))
