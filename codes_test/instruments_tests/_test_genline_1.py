from instruments import *
from numpy.random import randint

notes = []
chord_types = []
for _ in range(1):
    notes.append(Note().set_vector(named_nnrel=NAMED_NNREL_LIN[randint(0, M)], accidental=randint(-2, 3)))
    chord_types.append(list(CHORD_TYPE_NS0_TO_NS1[NGS].keys())[randint(0, len(CHORD_TYPE_NS0_TO_NS1[NGS]))])

print(notes)
print(chord_types)

chords = [Chord(note.get_name(show_register=False) + ' ' + chord_type).set_printoptions(ns=1) for note, chord_type in zip(notes, chord_types)]

GenLine(chords).plot(color_style='br357t')
plt.show()
