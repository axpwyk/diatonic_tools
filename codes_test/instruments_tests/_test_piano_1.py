import instruments as inst
from theories import *

chords = ['C7sus2/F', 'FM7(9, #11, 13)', 'Db7(#9)/Ab']

fig, axs = inst.plt.subplots(len(chords), 1)
fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.01, hspace=0.01)
fig.set_figheight(12); fig.set_figwidth(36)

for ax, chord in zip(axs, chords):
    notes = Chord(chord).get_notes()
    if chord == 'FM7(9, #11, 13)':
        notes = [note.add_group(-1) for note in notes]
    inst.Piano(notes).plot(note_range=(-7, 16), ax=ax, title=chord)

inst.plt.savefig('test_piano_plot.svg', bbox_inches='tight', pad_inches=0.0)
