import os; os.chdir('../..')
from theories import *


def avoid_note(class_num):
    class_name = CLASS_LIST[class_num][0]
    # 7 modes of a scale
    ads = AlteredDiatonicScale('F' + ' ' + class_name)
    for k, tonic in zip([4, 1, 5, 2, 6, 3, 7], ['F', 'C', 'G', 'D', 'A', 'E', 'B']):
        # get type of current mode
        ads.set_scale_tonic_str(tonic)
        name = ads.get_name_old(2)[0]
        tonic = 'Cb' if name.find('#1')>0 else 'C#' if name.find('b1')>0 else 'C'
        par = scale_name_parser(name)
        type = par['scale_type']+par['altered_note'] if par['altered_note'] else par['scale_type']
        new_name = tonic + ' ' + type
        cs = ChordScale(new_name)

        # print Mode Name 1
        print(type, '\t', end='')

        # print Mode Name 2, 3
        conventional_names = ['---', '---']
        for i, cn in enumerate(cs.get_conventional_name()):
            conventional_names[i] = cn
        for cn in conventional_names:
            print(cn, '\t', end='')

        # print Base Chord
        print(cs.get_7th_chord().get_name_old(type_only=True), '\t', end='')

        # print fake dom7, fake m7, info
        _, info, fake_dom7, fake_m7 = cs.get_info()
        print(fake_dom7, '\t', end='')
        print(fake_m7, '\t', end='')
        for i in info:
            print(i, '\t', end='')

        # print Scale Pos, Mode Pos, Brightness
        print(class_num, '\t', k, '\t', cs.get_color(), end='')
        print()

for i in range(23):
    avoid_note(i)
