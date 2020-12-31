import os; os.chdir('../..')
from instruments import *

cs = ChordScale('Eb Dorian(#5)')
notes = list(cs)
labels, long_list, fake_dom7, fake_m7 = cs.get_info()
print(labels)
for label, note in zip(labels, notes):
    note.set_message(cstype=label)

p12 = Piano().set_notes(notes)
p12.plot_old(title='test')
plt.show()
