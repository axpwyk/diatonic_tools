import os; os.chdir('..')
from theories import *


def avoid_note(class_name='Mixolydian(b2)'):
    # class_name = CLASS_LIST[0][0]
    print(class_name, '\t', end='')

    ads = AlteredDiatonicScale('C ' + class_name)
    notes = ads.get_notes()

    itvs = [n-notes[0] for n in notes]
    degs = [INTERVAL_NAME_TO_TENSION_NAME[str(i)] for i in itvs]

    for i in [0, 2, 4, 6]:
        degs[i] = degs[i] + '-chord_note'

    if all(['R' in degs, '3' in degs, 'b7' in degs]):
        if '11' in degs:
            idx = degs.index('11')
            degs[idx] = degs[idx] + '-avoid_type_0'
    else:
        for i in range(1, len(notes)):
            if any([abs(notes[i]-notes[0])==1, abs(notes[i]-notes[2])==1, abs(notes[i]-notes[4])==1, abs(notes[i]-notes[6])==1]):
                degs[i] = degs[i] + '-avoid_type_1'
        if all(['R' in degs, 'b3' in degs, 'b7' in degs]):
            if '13' in degs:
                idx = degs.index('13')
                degs[idx] = degs[idx] + '-avoid_type_2'

    long_list = ['x'] * 12
    for i, n in enumerate(notes):
        long_list[abs(n)] = degs[i]

    return long_list


for class_name in sum([c[:7] for c in [CLASS_LIST[t] for t in range(23)]], []):
    long_list = avoid_note(class_name)
    for s in long_list:
        print(s, '\t', end='')
    print()
