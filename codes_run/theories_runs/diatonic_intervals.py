import os; os.chdir('..')
from theories import *

notes = []
for nnabs in NAMED_NOTES + [NAMED_NOTES[0]+N]:
    notes.append(Note().set_vector(nnabs%N, 0, nnabs//N))

intervals = [n2-n1 for n2, n1 in zip(notes[1:], notes[:-1])]


def cumsum(lst):
    out = []
    for i in range(len(intervals)):
        out.append(sum(lst[:i], Interval()))
    return out


for i in range(len(intervals)):
    print(cumsum(intervals[i:]+intervals[:i]))
