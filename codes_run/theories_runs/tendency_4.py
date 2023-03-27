from theories import *


def movements(prev_note, interval):
    key_centers = [(Note('Db') + Interval('P5') * k).set_vector(register=0) for k in range(N)]

    prev_notes = [prev_note.get_enharmonic_note_by_key_center(key_center) for key_center in key_centers]
    prev_itvs = [(pn - key_center).normalize() for pn, key_center in zip(prev_notes, key_centers)]
    prev_r357ts = [prev_itv.get_r357t() for prev_itv in prev_itvs]
    prev_stability = [0 if int(prev_itv) % N in [0, 3, 4, 7] else 1 for prev_itv in prev_itvs]

    next_notes = [(prev_note + interval).get_enharmonic_note_by_key_center(key_center) for key_center in key_centers]
    next_itvs = [(nn - key_center).normalize() for nn, key_center in zip(next_notes, key_centers)]
    next_r357ts = [next_itv.get_r357t() for next_itv in next_itvs]
    next_stability = [0 if int(next_itv) % N in [0, 3, 4, 7] else 1 for next_itv in next_itvs]

    key_center_names = [key_center.get_name(show_register=False) for key_center in key_centers]
    r357t_changes = [f'{pr357t}->{nr357t}' for pr357t, nr357t in zip(prev_r357ts, next_r357ts)]
    stability_changes = [f'{pstab}{nstab}' for pstab, nstab in zip(prev_stability, next_stability)]

    for i in range(12):
        print(key_center_names[i], end='\t')
    print()

    for i in range(12):
        print(r357t_changes[i], end='\t')
    print()

    for i in range(12):
        print(stability_changes[i], end='\t')
    print()

    for ab in ['00', '01', '10', '11']:
        print(f'{ab}: {stability_changes.count(ab)}', end='\t')
    print()


for itv in ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'A4', 'P5', 'm6', 'M6', 'm7', 'M7']:
    movements(Note('C'), Interval(itv))
