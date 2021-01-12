from theories import *

major_tonic = Note('C0')
phrygian_p5_tonic = major_tonic + Interval('P5')  # Note('G0')

notes = Chord('G 7')[:]
intervals = [note - major_tonic for note in notes]

notes_neg = [phrygian_p5_tonic - itv for itv in reversed(intervals)]
print(Chord().set_notes(body=notes_neg).set_printoptions(ns=1).get_name())
