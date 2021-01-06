from theories import *


def prints(c):
    print(c.get_name())
    print(c.__str__())
    print(c.__repr__())
    print(c.get_notes())


# Full Chord
c = Chord('Em7(9, 11, 13)/F#').set_printoptions(ns=1)
prints(c)
print()

# Tanaka aug 1
c = Chord('Caug/F#').set_printoptions(ns=1)
prints(c)
print()

# Tanaka aug 2
c = Chord('F# 1.b5.b7.9').set_printoptions(ns=0)
prints(c)
print()

# diy chord
c = Chord().set_notes(body=AlteredDiatonicScale('C Ionian(#5)').get_chord_ex((0, 2, 4, 6))).set_printoptions(ns=1)
prints(c)
print()

# diatonic chords
for deg in range(M):
    notes = AlteredDiatonicScale('A Aeolian(#3)').get_chord(deg, 7)
    print(Chord().set_notes(body=notes[:4], tension=notes[4:]).set_printoptions(ns=1).get_name())
print()

# tension -> body
print(Chord().set_notes(body=Chord('EM7(9, 11, 13)').get_notes(tension_only=True)).set_printoptions(ns=1).get_name())
