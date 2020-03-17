from theories import *

print(Interval(-1, 0).get_name())
print(Interval(12, 6).get_name())
print(Interval(-7, -13).get_name())
print(Interval(12, -1).get_name())
print()

itv1 = Interval()._from_name('d1')
print(itv1, -itv1)
print(itv1.get_delta_note())
print(itv1.get_delta_step())

itv2 = Interval()._from_name('d8')
print(itv2, -itv2)
print(itv2.get_delta_note())
print(itv2.get_delta_step())

itv3 = Interval()._from_name('-d1')
print(itv3, -itv3)
print(itv3.get_delta_note())
print(itv3.get_delta_step())

itv4 = Interval()._from_name('-d8')
print(itv4, -itv4)
print(itv4.get_delta_note())
print(itv4.get_delta_step())
