from theories import *
from utils_io import dict2csv


notes = [Note('Db').add_generator(k) for k in range(12)]
diatonic_scales = [DiatonicScale('C E-mode').add_accidental(k) for k in range(6)]
tendencies = [Interval('-M2'), Interval('-m2'), Interval('P1'), Interval('m2'), Interval('M2')]

chart = [[], [], [], [], [], [], [], [], [], [], [], []]
for ds in diatonic_scales:
    ds_notes = [note.get_name(show_register=False) for note in ds]
    stable_notes = [ds_notes[i] for i in [0, 2, 4]]
    for k, note in enumerate(notes):
        for tendency in tendencies:
            note_moving = note.get_name(show_register=False)
            note_moved = (note + tendency).get_name(show_register=False)
            if note_moving in ds_notes and note_moved in stable_notes:
                chart[k].append(1)
            else:
                chart[k].append(0)

for i in range(len(chart[0])):
    row_i = {k: v[i] for k, v in zip([note.get_name(show_register=False) for note in notes], chart)}
    dict2csv(row_i, 'chart.csv', False)
