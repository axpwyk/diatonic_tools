from theories import *

chord = Chord().set_notes(body=[Note('F').add_gidx(k) for k in range(7)])
print(chord.get_name())
print(chord)
print()
print(chord.get_sorted_chord().get_name())
print(chord.get_sorted_chord())
print()

roots = [get_chromatic_polar_notes()[0].add_gidx(n) for n in range(12)]
roots.sort(key=lambda note: note.get_nnabs())
augs = [Chord().set_notes(body=[(root + k * Interval('M3')).get_enharmonic_note_by_key_center() for k in range(3)]).get_sorted_chord() for root in roots]
dim7s = [Chord().set_notes(body=[(root + k * Interval('m3')).get_enharmonic_note_by_key_center() for k in range(4)]).get_sorted_chord() for root in roots]
dom7b9s = [Chord().set_notes(body=[root + itv for itv in Chord('C 7(b9)').get_intervals_cum()]).get_sorted_chord() for root in roots]
# print(augs)
# print(dim7s)
print(dom7b9s)

# print([aug.get_major_converged_chord() for aug in augs])
# print([dim7.get_major_converged_chord() for dim7 in dim7s])

for dom7b9 in dom7b9s:
    print(dom7b9.get_notes(), ' -> ', dom7b9.get_major_converged_chord().get_notes())