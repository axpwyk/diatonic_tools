import os; os.chdir('../..')
from theories import *

# [N, G, S] = [97, 26, 0]

# itv1 = Interval('M16')
# itvs = []
# for i in range(28):
#     tmp = itv1 * i
#     itvs.append(tmp.normalize())
#
# print(itvs)
#
# itvs = []
# for i in range(28):
#     tmp = itv1 * -i
#     itvs.append(tmp.normalize())
#
# print(itvs)

intervals = []

ds = DiatonicScale('A A-mode')
print(ds)

for note in ds:
    intervals.append(note - ds[0])
print(intervals)

intervals = []

ds = DiatonicScale('A L-mode')
print(ds)

for note in ds:
    intervals.append(note - ds[0])
print(intervals)

