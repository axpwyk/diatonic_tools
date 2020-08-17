import os; os.chdir('../..')
from theories import *

itv1 = Interval('-d2')
itv2 = Interval('-d1')
itv3 = Interval('-dd2')
note1 = Note('C2')
note2 = Note('B##1')
note3 = Note('B##0')

print(itv1, itv2)
print()

print(itv1 + itv1)
print(itv2 + itv2)
print()

print(itv1.normalize())
print()

print(note1 - note2)
print(note2 - note1)
print()

print(note1 - note3)
print(note3 - note1)
print()

print(note2 - note3)
print(note3 - note2)
print()

print(note1 - note2 + note3)
print()

print(Interval('m3') + Interval('M3'))
print()

print(Interval('m3') - Interval('M3'))
print()

print(Interval('M3') - Interval('m3'))
print()
