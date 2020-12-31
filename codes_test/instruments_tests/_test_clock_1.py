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


# get_scale('F Dorian', 5, save_name='F Dorian')
# get_scale('F Dorian', colorize=(5, 8, 0, 3), save_name='Fm7 in F Dorian')
# get_scale('F Dorian', colorize=(7, 10, 2, 5), save_name='Gm7 in F Dorian')
# get_scale('F Dorian', colorize=(0, 3, 7, 10), save_name='Cm7 in F Dorian')
# get_chord('Fm7', save_name='Fm7 in F Dorian 2')
# get_chord('Gm7', save_name='Gm7 in F Dorian 2')
# get_chord('Cm7', save_name='Cm7 in F Dorian 2')

# get_scale('B Locrian(b7)', 11, None, 'B Locrian(b7)')
# get_scale('B Locrian(b7)', None, (11, 2, 5, 8), 'Bdim7 in B Locrian(b7)')
# get_chord('Bdim7', None, None, 'Bdim7 in B Locrian(b7) 2')

# get_scale('A Aeolian(#7)', 9, None, 'A Aeolian(#7)')
# get_scale('A Aeolian(#7)', None, (8, 11, 2, 5), 'G#dim7 in A Aeolian(#7)')
# get_chord('G#dim7', None, None, 'G#dim7 in A Aeolian(#7) 2')

# get_scale('E Phrygian(#3)', 4, None, 'E Phrygian(#3)')
# get_chord('G7+5(9)')
# get_chord('Eaug/Bb')


# get_scale('C Ionian', 0, 'degree', None, 'C Ionian')
# get_scale('Eb Ionian', 3, 'degree', None, 'Eb Ionian')
# get_scale('C Lydian', 0, 'degree', None, 'C Lydian')
# get_scale('C Aeolian(#7)', 0, 'degree', None, 'C Aeolian(#7)')

# get_scale('C Ionian(b2, #4, #5, #6)')
get_chord('Ebm(9, 13)')
