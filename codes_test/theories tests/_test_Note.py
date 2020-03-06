from theories import *

note = Note()._from_name('C0')
interval_name = 'm2'

print(note._get_name(), note)

for _ in range(12):
    note.add_interval(interval_name)
    print(note._get_name(), note)

print('-------------------------')

print(note._get_name(), note)

for _ in range(12):
    note.sub_interval(interval_name)
    print(note._get_name(), note)
