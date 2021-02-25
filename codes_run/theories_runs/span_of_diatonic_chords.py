from theories import *

ds = DiatonicScale()

for i in range(7):
    ch = ds.get_chord(i, 7)
    print(Chord().set_notes(body=ch).get_name(), '\t', get_span(ch), '\t', get_polar(ch))
