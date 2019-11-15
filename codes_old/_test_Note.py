from theories import *

note = Note().from_name('C0')
interval_name = 'm2'

print(note.to_name(), note)

for _ in range(12):
    note.add_interval(interval_name)
    print(note.to_name(), note)

print('-------------------------')

print(note.to_name(), note)

for _ in range(12):
    note.sub_interval(interval_name)
    print(note.to_name(), note)
