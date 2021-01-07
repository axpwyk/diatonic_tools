from itertools import cycle
from instruments import *

intervals = [Interval('M2'), Interval('M2'), Interval('M2'), Interval('m2')]
intervals_cycle = cycle(intervals)

c = [Note('C')]
for _ in range(20):
    c.append(c[-1] + next(intervals_cycle))

for note in c:
    note.set_message(br357t=(note - c[0]).get_r357t())

Piano().set_notes(c).plot()
plt.show()
