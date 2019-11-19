from termcolor import cprint
from theories import *

s = Mode('Db Locrian')

for i in range(21):
    print('{:14s}'.format(s.mode()), end='')

    print('[', end='')
    # for t in s.scale:
    #     print('{:4s}'.format(triple2note(t)), end='')
    for t in range(7):
        chord, chord_type = s.get_chord_from_steps([k % 7 for k in [0 + t, 2 + t, 4 + t, 6 + t, 8 + t]])
        chord_name = triple_to_note_name(chord[0])

        cprint('{:8s}'.format(chord_name+chord_type), CHORD_COLOR_CONSOLE[chord_type], end='')
    print(']', end='')
    print()

    s.add_sharp()
