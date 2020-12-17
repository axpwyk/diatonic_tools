import numpy as np


def is_isomorphic(list1, list2):
    if len(list1) != len(list2): return False
    def l_shift(l, k):
        return l[k:] + l[:k]
    def distance(list1, list2):
        return sum([abs(l1-l2) for l1, l2 in zip(list1, list2)])
    for k in range(len(list1)):
        if distance(l_shift(list1, k), list2) == 0:
            return True
        else:
            continue
    return False


chords = [[0, 1, 2]]
for i in range(12):
    for j in range(i+1, 12):
        for k in range(j+1, 12):
            cur_chord = [i, j, k]
            cur_chord_appended = cur_chord + [cur_chord[0]+12]
            cur_intervals = [c2-c1 for c1, c2 in zip(cur_chord_appended[:-1], cur_chord_appended[1:])]
            bool_list = []
            for cmp_chord in chords:
                cmp_chord_appended = cmp_chord + [cmp_chord[0]+12]
                cmp_intervals = [c2-c1 for c1, c2 in zip(cmp_chord_appended[:-1], cmp_chord_appended[1:])]
                print(cur_intervals, cmp_intervals)
                if is_isomorphic(cur_intervals, cmp_intervals):
                    bool_list.append(True)
                else: bool_list.append(False)
            if any(bool_list):
                continue
            else: chords.append(cur_chord)
print(chords)
print(len(chords))
