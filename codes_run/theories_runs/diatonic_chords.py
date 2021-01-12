from theories import *

ds = DiatonicScale('F# Locrian')

for _ in range(7):
    ds.add_accidental(-1)
    print(ds.get_name(), end='\t')
    for deg in range(7):
        print(Chord().set_notes(body=ds.get_chord(deg, 4)).set_printoptions(ns=1).get_name(), end='\t')
    print()
