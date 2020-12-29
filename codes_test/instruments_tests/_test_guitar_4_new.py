import os; os.chdir('../..')
from instruments import *

chord_name = 'F#m7'
file_name = copy(chord_name).replace('/', '_on_').replace('5(9)', 'sus2')
chord = Chord(chord_name)
notes = chord.get_notes()
# notes.pop(2)

g = Guitar(open_string_notes=(Note('E1'), Note('A1'), Note('D2'), Note('G2'), Note('B2'), Note('E3'))).add_notes(notes)
# g = Guitar(open_string_notes=(Note('C#1'), Note('G#1'), Note('E2'), Note('F#2'), Note('B2'), Note('E3'))).add_notes(notes)

g.plot_all_chords(text_style='br357t', title=chord_name)
plt.savefig(f'outputs/{file_name}.svg', bbox_inches='tight')
