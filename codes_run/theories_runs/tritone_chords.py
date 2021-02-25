from theories import *
from itertools import product
import pandas as pd


def get_dom7(lower_d5):
    return Chord().set_notes(body=[lower_d5 - Interval('M3'), lower_d5, lower_d5 + Interval('m3'), lower_d5 + Interval('d5')])


def get_m69(lower_d5):
    higher_d5 = lower_d5 + Interval('d5') - Interval('P8')
    return Chord().set_notes(body=[higher_d5 - Interval('m3'), higher_d5, higher_d5 + Interval('M3'), lower_d5])


def get_aug_on_sharp_4(lower_d5):
    higher_d5 = lower_d5 + Interval('d5')
    return Chord().set_notes(bass=[lower_d5], body=[higher_d5, higher_d5 + Interval('M3'), higher_d5 + 2 * Interval('M3')])


def get_aug_on_sharp_6(lower_d5):
    higher_d5 = lower_d5 + Interval('d5')
    return Chord().set_notes(bass=[lower_d5], body=[higher_d5 - Interval('M3'), higher_d5, higher_d5 + Interval('M3')])


def get_aug_on_2(lower_d5):
    higher_d5 = lower_d5 + Interval('d5') + Interval('P8')
    return Chord().set_notes(bass=[lower_d5], body=[higher_d5 - 2 * Interval('M3'), higher_d5 - Interval('M3'), higher_d5])


itvs = [Interval('-d3'), Interval('-M2'), Interval('-m2'), Interval('-d2'), Interval('-A1'), Interval('P1'), Interval('A1'), Interval('d2'), Interval('m2'), Interval('M2'), Interval('d3')]
n1 = Note('B0')
n2 = Note('F1')

print(get_dom7(n1))
print(get_m69(n1))
print(get_aug_on_sharp_4(n1))
print(get_aug_on_sharp_6(n1))
print(get_aug_on_2(n1))

# df = pd.DataFrame(columns=['itv1', 'itv2', 'n1', 'n2', 'itv', 'n_ht'])
# for i1, i2 in product(itvs, repeat=2):
#     n1_ = n1 + i1
#     n2_ = n2 + i2
#     if 'A' not in (n2_ - n1_).get_name() and 'd' not in (n2_ - n1_).get_name():
#         df = df.append({'itv1': i1, 'itv2': i2, 'n1': n1_, 'n2': n2_, 'itv': n2_ - n1_, 'n_ht': int(n2_ - n1_)}, ignore_index=True)
# df.to_csv('tritone_chords.csv', index=False)
