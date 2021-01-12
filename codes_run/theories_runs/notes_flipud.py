from theories import *

notes = DiatonicScale('C Ionian')[:]
mirror_note = Note('D')

intervals = [note - mirror_note for note in notes]
print(intervals)

notes_flipud = [mirror_note - itv for itv in intervals]
print(notes_flipud)
