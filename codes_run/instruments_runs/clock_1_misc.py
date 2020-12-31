from instruments import *


def get_chord(chord_name, tonic=None, margin_anno_type='', colorize=None, save_name=''):
    clock = Clock(Chord(chord_name).get_notes())
    clock.plot(chord_name.replace('#', r'$\sharp$').replace('b', r'$\flat$'),
               tonic=tonic, interval_anno_style=margin_anno_type, colorize=colorize)
    if save_name:
        plt.savefig(save_name+'.svg', bbox_inches='tight', pad_inches=0.0)
    else:
        plt.savefig('三个和弦的键盘示意图.svg', bbox_inches='tight', pad_inches=0.0)


def get_scale(scale_name, tonic=None, margin_anno_type='', colorize=None, save_name=''):
    clock = Clock(AlteredDiatonicScale(scale_name).get_notes())
    clock.plot(scale_name.replace('#', r'$\sharp$').replace('b', r'$\flat$'),
               tonic=tonic, interval_anno_style=margin_anno_type, colorize=colorize)
    if save_name:
        plt.savefig(save_name+'.svg', bbox_inches='tight', pad_inches=0.0)
    else:
        plt.savefig('三个和弦的键盘示意图.svg', bbox_inches='tight', pad_inches=0.0)


# get_scale('C Ionian', 0, 'degree', None, '1-1 C Ionian')
# get_scale('Eb Ionian', 3, 'degree', None, '1-2 Eb Ionian')
# get_scale('C Lydian', 0, 'degree', None, '1-3 C Lydian')
# get_scale('C Aeolian(#7)', 0, 'degree', None, '1-4 C Aeolian(#7)')

# get_scale('F Dorian', 5, 'degree', None, '2-1 F Dorian')
# get_chord('Fm7', None, 'degree', None, '2-2 Fm7')
# get_chord('Gm7', None, 'degree', None, '2-3 Gm7')
# get_chord('Cm7', None, 'degree', None, '2-4 Cm7')

# get_scale('A Aeolian(#7)', 9, 'degree', None, '3-1 A Aeolian(#7)')
# get_chord('G#dim7', None, 'degree', None, '3-2 G#dim7')
# get_scale('C Ionian(b6)', 0, 'degree', None, '3-3 C Ionian(b6)')
# get_chord('Bdim7', None, 'degree', None, '3-4 Bdim7')

# get_scale('A Aeolian(#7)', 9, 'degree', None, '5-1 A Aeolian(+7)')
# get_scale('E Phrygian(#3)', 4, 'degree', None, '5-2 E Phrygian(+3)')
