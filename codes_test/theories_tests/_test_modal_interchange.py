from theories import *

def print_diatonic_chords(mode):
    for i in range(7):
        print(mode.get_full_chord(i).get_name(), end='\t')
    print('')

roots = ['D#', 'D', 'Db']
mode_types = ['Lydian', 'Ionian', 'Mixolydian', 'Dorian', 'Aeolian', 'Phrygian', 'Locrian']
for root in roots:
    for mode_type in mode_types:
        mode = Mode(root+' '+mode_type)
        print(mode.get_name(), end='\t')
        print_diatonic_chords(mode)
