from instruments import *


def get_chord(chord_name='Caug/F#', selection='x9a99x', fret_interval=(7, 11), save_name=''):
    par = chord_name_parser(chord_name)
    if par['bass_name']:
        g = Guitar(Chord(chord_name)[0:])
    else:
        g = Guitar(Chord(chord_name)[1:])
    g.select(selection)
    g.plot2(*fret_interval, title=chord_name.replace('#', r'$\sharp$').replace('b', r'$\flat$'))
    if not save_name:
        plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
    if save_name:
        plt.savefig(f'{fret_interval[0]}-{fret_interval[1]}_'+save_name, bbox_inches='tight', pad_inches=0.0)


def get_scale(scale_name='C Dorian', fret_interval=(0, 12), save_name=''):
    g = Guitar(AlteredDiatonicScale(scale_name).get_notes())
    g.plot2(*fret_interval, title=scale_name.replace('#', r'$\sharp$').replace('b', r'$\flat$'))
    if not save_name:
        plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)
    if save_name:
        plt.savefig(f'{fret_interval[0]}-{fret_interval[1]}_'+save_name, bbox_inches='tight', pad_inches=0.0)


# get_chord('Caug/F#', '', (0, 12), 'Caug-on-F#.svg')
# get_chord('Caug/F#', 'x9a99x', (7, 11), 'Caug-on-F#.svg')
# get_chord('GM7', '', (0, 12), 'GM7.svg')
# get_chord('GM7', 'xx5777', (2, 6), 'GM7.svg')
get_chord('Dm7(9, 11, 13)', '', (0, 12), 'Dm7(9, 11, 13).svg')
get_chord('Dm7', 'x57700', (4, 8), 'Dm7.svg')

# get_chord('C', 'x32010', (0, 4), 'C0.svg')
# get_chord('C', 'x35553', (2, 6), 'C2.svg')
# get_chord('Ab7', '', (0, 12), 'Ab7.svg')
# get_chord('G#7', '', (0, 12), 'G#7.svg')
# get_chord('Caug/F#', 'x9a99x', (7, 11), 'Caug-on-F#7.svg')
# get_chord('F', 'x8aaa8', (7, 11), 'F7.svg')

# get_scale('C Lydian(b6)', (0, 7), 'C-Lydian(b6).svg')

# get_chord('Cm6(9)', '', (7, 11), 'Cm69.svg')
# get_chord('E6', '0b9999', (8, 12), 'E6.svg')
# get_chord('AM7(#11)', 'x01120', (0, 4), 'AM7(#11).svg')
# get_chord('Dbm7-5(11)', 'x44000', (2, 6))

# get_scale('C Phrygian(#3)', (0, 12), 'C Phrygian(#3).svg')
# get_scale('C Lydian(b6)', (0, 12), 'C Lydian(b6).svg')
# get_chord('Bsus2', '', (0, 12), 'Bsus2.svg')
# get_chord('Bsus2', 'x24422', (0, 4), 'Bsus2.svg')

# yozora
# get_chord('E', '022100', (0, 4), 'E.svg')
# get_chord('Bsus2', 'x24422', (0, 4), 'Bsus2.svg')
# get_chord('B#dim', 'x3454x', (2, 6), 'B#dim.svg')
# get_chord('C#m7', 'x46600', (3, 7), 'C#m7.svg')

