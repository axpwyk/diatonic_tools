import os; os.chdir('..')
from theories import *

# collect notes of 2 chords
notes = Chord('C').get_notes()+Chord('F#').get_notes()

# make unique note list
notes_used = []
notes_unique = []
for note in notes:
    if abs(note) % 12 not in notes_used:
        notes_unique.append(note)
    else:
        continue
    notes_used.append(abs(note) % 12)
notes_unique.sort(key=lambda x: abs(x) % 12)
print(notes_unique)

# generate AlteredDiatonicScale from note list
if len(notes_unique) == 7:
    pass
elif len(notes_unique) < 7:
    pass
elif len(notes_unique) > 7:
    print('len(notes_unique) must not larger than 7.')
