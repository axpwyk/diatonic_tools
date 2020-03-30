from theories import *


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


def is_equal(list_1, list_2):
    if len(list_1) != len(list_2): return False
    def _dist(l1, l2):
        return sum([abs(i-j) for i, j in zip(l1, l2)])

    if _dist(list_1, list_2) < 1e-5: return True
    else: return False


intervals_list = []
with open('all_heptatonic_scale_intervals.txt', 'r') as f:
    for line in f:
        intervals_list.append(eval(line))


# scale = [Note('Cb0'), Note('Db0'), Note('Eb0'), Note('Fb0'), Note('Gb0'), Note('Ab0'), Note('Bbb0')]
# scale.append(scale[0]+Interval('P8'))
# intervals = [n2-n1 for n1, n2 in zip(scale[:-1], scale[1:])]
# print(intervals)
# intervals = [abs(interval) for interval in intervals]
scale = AlteredDiatonicScale('C Lydian(#5,#6)')
intervals = scale.get_interval_vector()
root = scale[0].get_name()
bools = [is_isomorphic(intervals, intervals_list[k]) for k in range(66)]
idx = bools.index(True)


class_idx = []
with open('all_heptatonic_scale_classes.txt', 'r') as f:
    for i, line in enumerate(f):
        if i == idx: class_idx.extend(eval(line))
step = len(class_idx)//7
# from the least accidentals to the most accidentals, return at most 5 nearest scales
class_idx_reshuffle = [[class_idx[s+step*k] for k in range(7)] for s in range(step)]
class_idx_reshuffle = class_idx_reshuffle[:5]
class_idx_reshuffle_intervals = [[AlteredDiatonicScale('C '+scale).get_interval_vector() for scale in r] for r in class_idx_reshuffle]
indices = []
for r in class_idx_reshuffle_intervals:
    bools = [is_equal(intervals, c) for c in r]
    if any(bools):
        indices.append(bools.index(True))
top_5_scales = [class_idx_reshuffle[j][i] for j, i in enumerate(indices)]
print(f'Class={idx}, root={root}, type={top_5_scales}')
