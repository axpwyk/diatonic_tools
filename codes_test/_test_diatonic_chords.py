from termcolor import cprint
from theories import *

s = Tonality('Ab Locrian')

for i in range(21):
    print('{:14s}'.format(s.tonality()), end='')

    print('[', end='')
    # for t in s.scale:
    #     print('{:4s}'.format(triple2note(t)), end='')
    for t in range(7):
        chord, chord_type = s.chord(t)
        chord_name = triple_to_note_name(chord[0])

        cprint('{:8s}'.format(chord_name+chord_type), CHORD_TYPE_COLORS[chord_type], end='')
    print(']', end='')
    print()

    s.add_sharp()
