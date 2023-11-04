from theories import *
from utils_io import *

notes = [(Note('Gb')+k*Interval('P5')).set_vector(register=0) for k in range(2*N-M)]
offset_bottom = -7
offset_top = 3
notes_ex = [(Note('Gb')+k*Interval('P5')).set_vector(register=0) for k in range(offset_bottom, 2*N-M+offset_top)]
out_dict = {}
print(notes_ex)

# MAKE DICT
def make_dict(chord_name):
    chord_notes = Chord(chord_name)
    chord_span = get_span(chord_notes, enharmonic=True)
    polar_notes = get_polar(chord_notes, enharmonic=True)
    chord_lower_poles = [x[0].get_name(False) for x in polar_notes]
    chord_upper_poles = [x[1].get_name(False) for x in polar_notes]
    dict_tmp = {
        'chord_name': chord_notes.get_name(),
        'chord_notes': ', '.join([chord_note.get_name(False) for chord_note in chord_notes]),
        'chord_root': chord_notes[0].get_name(False),
        'chord_span': chord_span,
        'chord_lower_pole': ', '.join(chord_lower_poles),
        'chord_upper_pole': ', '.join(chord_upper_poles),
        'chord_mass_center': Note('F').add_gidx(int(sum([chord_note.get_gidx() for chord_note in chord_notes]) / len(chord_notes))).get_name(False)
    }
    for note in notes:
        new_span = get_span([*chord_notes, note], enharmonic=True)
        dict_tmp = {**dict_tmp, 'tension_note': note.get_name(False)}
        dict_tmp = {**dict_tmp, 'tension_position': (note-chord_notes[0]).normalize().get_r357t()}
        dict_tmp = {**dict_tmp, 'new_span': new_span}
        itvs = [int(note - chord_note) % N for chord_note in chord_notes]
        # chord notes // [T0], red
        if 0 in itvs:
            dict_tmp = {**dict_tmp, 'tension_type': 'T0'}
            dict2csv(dict_tmp, 'diatonic_tensions.csv', False)
            continue

        # from the most unacceptable to the most acceptable

        # m2 above avoids (except dominant 7th chord, minor chord R, P5) // [T5], black
        if1 = 1 in itvs
        if2 = chord_span < M - 1
        if3 = 'm3' in [(chord_note - chord_notes[0]).normalize() for chord_note in chord_notes]
        if4 = (int(note - chord_notes[0]) - 1) % N not in [0, G]
        if all([if1, if2, not if3 or (if3 and if4)]):
            dict_tmp = {**dict_tmp, 'tension_type': 'T5'}
        # natural and altered at same time // [T4], gray
        elif note.get_named_nnrel() in [chord_note.get_named_nnrel() for chord_note in chord_notes]:
            dict_tmp = {**dict_tmp, 'tension_type': 'T4'}
        # m2 above minor chord R, P5 // [T3], blue
        elif ('m3' in [(chord_note - chord_notes[0]).normalize() for chord_note in chord_notes]) and ((int(note - chord_notes[0]) - 1) % N in [0, G]):
            dict_tmp = {**dict_tmp, 'tension_type': 'T3'}
        # enlarge span // [T2], orange
        elif new_span > chord_span:
            dict_tmp = {**dict_tmp, 'tension_type': 'T2'}
        else:
            # available // [T1], green
            dict_tmp = {**dict_tmp, 'tension_type': 'T1'}
        dict2csv(dict_tmp, 'diatonic_tensions.csv', False)


for j, quality in enumerate(['aug4', '4', 'm4', 'dim4', 'augM7sus4', 'M7sus4', 'sus4',
                             'augM7', 'aug7', 'aug', 'M7', '7', '6', '', 'M7-5', '7-5',
                             'm7+5', 'mM7', 'm7', 'm6', 'm', 'mM7-5', 'm7-5', 'dim7', 'dim',
                             'M7sus2', '7sus2', '7-5sus2', '6-5sus2', 'sus2']):
    for i, note in enumerate(notes_ex):
        make_dict(f'{note.get_name(show_register=False)} {quality}')

'''
红色：和弦内音
黑色：和弦内音上方小二度（跨度大于等于属七和弦除外，小和弦主音属音上方小二度除外）
灰色：自然音和变化音同时存在
蓝色：小和弦主音属音上方小二度
橙色：可用 tension，但会扩大和弦整体跨度
绿色：可用 tension，不会扩大和弦整体跨度
'''