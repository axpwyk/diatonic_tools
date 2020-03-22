from theories import *


def is_isomorphic(notes_1, notes_2):
    # first we compare the length of two sequences
    if len(notes_1) != len(notes_2):
        return False

    # calculate interval sequences
    notes_1_ = notes_1 + [notes_1[0]+Interval('P8')]
    interval_seq_1 = [n2-n1 for n1, n2 in zip(notes_1_[:-1], notes_1_[1:])]
    notes_2_ = notes_2 + [notes_2[0]+Interval('P8')]
    interval_seq_2 = [n2-n1 for n1, n2 in zip(notes_2_[:-1], notes_2_[1:])]

    # compare interval sequences
    def _r_shift(l, k):
        return l[-k:] + l[:-k]

    def _dist(l1, l2):
        return sum([abs(abs(l1_i) - abs(l2_i)) for l1_i, l2_i in zip(l1, l2)])

    for i in range(len(interval_seq_1)):
        if _dist(_r_shift(interval_seq_1, i), interval_seq_2) <= 0:
            return True
        else: pass

    return False


def in_scale_list(scale, scale_list):
    scale_notes = AlteredDiatonicScale(scale).get_notes()
    scale_list_notes = [AlteredDiatonicScale(s).get_notes() for s in scale_list]
    bools = [is_isomorphic(scale_notes, notes) for notes in scale_list_notes]
    return bools


scale = 'B Locrian(b4, b7)'
scale_list = ['Lydian', 'Lydian(#2)', 'Lydian(#3)', 'Lydian(#5)', 'Lydian(b7)', 'Lydian(#6)', 'Lydian(b2)', 'Lydian(b3)', 'Lydian(b6)', 'Lydian(#2,#3)', 'Lydian(#2,#6)', 'Lydian(#2,b6)', 'Lydian(#2,b7)', 'Lydian(#3,#6)', 'Lydian(#3,b2)', 'Lydian(#3,b6)', 'Lydian(#3,b7)', 'Lydian(#5,#6)', 'Lydian(#5,b2)', 'Lydian(#5,b3)', 'Lydian(#6,b2)', 'Lydian(#6,b3)', 'Lydian(b2,b3)', 'Lydian(b2,b6)']
scale_list = ['C '+s for s in scale_list]

print(in_scale_list(scale, scale_list))
idx = in_scale_list(scale, scale_list).index(True)
print(scale_list[idx])
