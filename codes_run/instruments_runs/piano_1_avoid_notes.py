import os; os.chdir('../..')
import instruments as inst
from theories import *

scale = 'C Ionian(#6)'
cs = ChordScale(scale)
notes = cs.get_notes()
labels, _, _, _ = cs.get_info()

# for altered
# notes[2] = notes[2].get_enharmonic_note()
# notes[3] = notes[3].get_enharmonic_note()
# notes[4] = notes[4].get_enharmonic_note()
# labels = ['[CN]', '[TN]', '[TN]', '[CN]', '[TN]', '[TN]', '[CN]']

for i in range(len(notes)):
    notes[i].set_message(cstype=labels[i])

piano = inst.Piano(notes + [Note('C#3').set_message(cstype='[TN]')])
piano.plot_old(title=scale)


# notes = [Note('A1').set_message('B'), Note('C#2').set_message('B'), Note('G2').set_message('B'), Note('D3'), Note('F#3')]
# inst.Piano(notes).plot(title='$\mathrm{A}7(11, 13)$')

# notes = [Note('A1').set_message('B'), Note('C#2').set_message('B'), Note('G2').set_message('B'), Note('C3'), Note('E3')]
# inst.Piano(notes).plot(title='$\mathrm{A}7(\sharp9)$')

inst.plt.savefig(f'outputs/{scale}.svg', bbox_inches='tight', pad_inches=0.0)
