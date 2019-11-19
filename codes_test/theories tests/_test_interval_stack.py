from theories import *

base = Note('E1')

m2 = Interval('m2')
M2 = Interval('M2')
A2 = Interval('A2')
m3 = Interval('m3')
M3 = Interval('M3')
P4 = Interval('P4')
A4 = Interval('A4')
d5 = Interval('d5')
P5 = Interval('P5')
m6 = Interval('m6')
M6 = Interval('M6')
m7 = Interval('m7')
M7 = Interval('M7')

notes = [base]
intervals = [m2, A2, m2, M2, m2, A2, m2]
for interval in intervals:
    notes.append(notes[-1]+interval)

print(notes)
