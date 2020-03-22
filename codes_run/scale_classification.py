import itertools
from copy import deepcopy
import sys
import numpy as np
from theories import *
import time


class Timer(object):
    def __init__(self):
        self._t = 0.0
        self._records = []

    def start(self):
        self._t = time.time()
        return self

    def record(self):
        self._records.append(time.time()-self._t)
        return self

    def reset(self):
        self._t = 0.0
        self._records = []
        return self

    def get(self):
        return self._records


def is_isomorphic(list_1, list_2):
    # first we compare the length of two sequences
    if len(list_1) != len(list_2): return False

    # calculate circular
    # list_1_fft = np.fft.fft(np.diff(list_1, append=list_1[0]))
    # list_2_fft = np.fft.fft(np.diff(list_2, append=list_2[0]))
    # d = np.linalg.norm(abs(list_1_fft)-abs(list_2_fft))
    # if d > 1e-5: return False

    # compare interval sequences
    def _l_shift(li, k):
        return li[k:] + li[:k]

    def _dist(l1, l2):
        return sum([abs(i-j) for i, j in zip(l1, l2)])

    for i in range(len(list_1)):
        if _dist(_l_shift(list_1, i), list_2) < 1e-5:
            return True
        else: pass

    return False


def scale_classes(n_accidentals=2):
    def _l_shift(li, k):
        return li[k:] + li[:k]

    offset=0
    base_diatonic_modes = ['Lydian', 'Ionian', 'Mixolydian', 'Dorian', 'Aeolian', 'Phrygian', 'Locrian']
    base_diatonic_modes = _l_shift(base_diatonic_modes, offset)
    accidentals = [''] + [f'#{k}' for k in range(1, 8)] + [f'b{k}' for k in range(1, 8)]

    results = []
    for mode in base_diatonic_modes:
        for accs in itertools.combinations_with_replacement(accidentals, n_accidentals):
            cur_mode = 'C' + ' ' + mode + '(' + ''.join([f'{acc},' for acc in accs[:-1]]) + accs[-1] + ')'
            cur_notes = [abs(note) for note in AlteredDiatonicScale(cur_mode).get_notes()]
            cur_notes.append(cur_notes[0]+12)
            cur_intervals = [n2-n1 for n1, n2 in zip(cur_notes[:-1], cur_notes[1:])]
            bool_illegal_interval = any([interval<=0 for interval in cur_intervals])
            if bool_illegal_interval:
                # print(f'Illegal interval occurred. Current mode {cur_mode} will be passed!')
                continue

            representative_modes = [x[0] for x in results]
            cmp_notes_list = [[abs(note) for note in AlteredDiatonicScale(cmp_mode).get_notes()] for cmp_mode in representative_modes]
            for cmp_notes in cmp_notes_list:
                cmp_notes.append(cmp_notes[0]+12)
            cmp_intervals_list = [[n2-n1 for n1, n2 in zip(cmp_notes[:-1], cmp_notes[1:])] for cmp_notes in cmp_notes_list]
            # print(cur_intervals)
            # print(cmp_intervals_list)

            bool_isomorphic = True in [is_isomorphic(cur_intervals, cmp_intervals) for cmp_intervals in cmp_intervals_list]
            if bool_isomorphic:
                idx = [is_isomorphic(cur_intervals, cmp_intervals) for cmp_intervals in cmp_intervals_list].index(True)
                results[idx].append(cur_mode)
            else: results.append([cur_mode])
    return results


results = scale_classes(2)
lengths = [len(class_k) for class_k in results]
steps = [length//7 for length in lengths]
for i, r in enumerate(results):
    print(f'----- CLASS {i} -----')
    step = steps[i]
    for times in range(step):
        print([r[times+step*k] for k in range(7)])
print(lengths)

# timer = Timer().start()
# all_scales = []
# for i in range(7):
#     results = scale_classes(i)
#     print(timer.record().get()[-1])
#     for result in results:
#         print(result[2:], end='\t')
#     print()
#     all_scales.append(results)
#
#
# isos = [deepcopy([]) for _ in range(len(all_scales[0]))]
# for t in range(len(all_scales[0])-1):
#     cur_scale = all_scales[0].pop(0)
#     print(cur_scale)
#     isos[t].append(cur_scale)
#     cur_scale_notes = AlteredDiatonicScale(cur_scale).get_notes()
#     for base in all_scales[1:]:
#         for i, cmp_scale in enumerate(base):
#             cmp_scale_notes = AlteredDiatonicScale(cmp_scale).get_notes()
#             if is_isomorphic(cur_scale_notes, cmp_scale_notes):
#                 isos[t].append(base.pop(i))
#                 continue
#             else: continue
# isos[-1].extend([s[0] for s in all_scales])
#
# for r in isos:
#     print(r)
#