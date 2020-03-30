from instruments import *


def get_chord(chord_name, tonic=None, margin_anno_type='', colorize=None, save_name=''):
    clock = Clock(Chord(chord_name).get_notes())
    clock.plot(chord_name.replace('#', r'$\sharp$').replace('b', r'$\flat$'),
               tonic=tonic, margin_anno_type=margin_anno_type, colorize=colorize)
    if save_name:
        plt.savefig(save_name, bbox_inches='tight', pad_inches=0.0)
    else:
        plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)


def get_scale(scale_name, tonic=None, margin_anno_type='', colorize=None, save_name=''):
    clock = Clock(AlteredDiatonicScale(scale_name).get_notes())
    clock.plot(scale_name.replace('#', r'$\sharp$').replace('b', r'$\flat$'),
               tonic=tonic, margin_anno_type=margin_anno_type, colorize=colorize)
    if save_name:
        plt.savefig(save_name, bbox_inches='tight', pad_inches=0.0)
    else:
        plt.savefig('debug.svg', bbox_inches='tight', pad_inches=0.0)


# get_scale('Eb Ionian(#5,#5,#6,b2,b3,b3,b4,b4)', 3, '', None, '9_heptatonic_sacle_of_order_8.svg')
get_scale('C Lydian(#5, #6)')
