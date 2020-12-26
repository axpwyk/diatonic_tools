import os; os.chdir('../..')
from instruments import *

cs = ChordScale('D Dorian')
notes = cs.get_notes()
labels, long_list, fake_dom7, fake_m7 = cs.get_info()
print(labels)
for label, note in zip(labels, notes):
    note.set_message(cstype=label)

p12 = PianoSpecial().set_notes(notes)
p12.plot(title='test')
plt.show()
