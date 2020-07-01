from theories import *

mode = ' mixolydian'
keys = [Note('Db'), Note('Gb'), Note('Ab'), Note('B'), Note('Eb'), Note('E'), Note('Bb'), Note('A'), Note('F'), Note('D'), Note('C'), Note('G')]

Gb_Ionian = [DiatonicScale('Gb Ionian')[n] for n in [0, 1, 2, 4, 5]]

print(end='\t\t')
for key in keys:
    print(key.get_name(show_group=False), end='\t')
print()

for note in Gb_Ionian:
    print(note.get_name(show_group=False), end='\t\t')
    for key in keys:
        key_vec = key.get_vector()
        note_vec = note.get_vector()
        if key_vec[0] == note_vec[0] and key_vec[1] != note_vec[1]:
            cur_interval = note.get_enharmonic_note() - key
        else:
            cur_interval = note - key
        cur_interval.normalize()

        replace_dict = {'P1': 'R', 'A1': 'b9', 'm2': 'b9', 'M2': '9', 'd3': '9', 'm3': '#9(m3)',
                        'M3': '3', 'd4': '3', 'P4': '11', 'd5': '#11(-5)', 'P5': '5', 'd6': '5',
                        'm6': 'b13(#5)', 'M6': '13', 'd7': '13', 'm7': '7', 'M7': '##13(M7)'}

        print(f'{replace_dict[cur_interval.get_name()]}', end='\t')
    print()
