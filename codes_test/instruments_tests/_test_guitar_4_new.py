import os; os.chdir('../..')
from instruments import *

chord_name = 'FM7-5/C'
file_name = copy(chord_name).replace('/', '_on_').replace('5(9)', 'sus2')
chord = Chord(chord_name)
notes = chord.get_notes()
# notes.pop(2)

g = Guitar(open_string_notes=(Note('B0'), Note('E1'), Note('A1'), Note('D2'), Note('G2'), Note('B2'), Note('E3'))).add_notes(notes)
# g = Guitar(open_string_notes=(Note('C#1'), Note('G#1'), Note('E2'), Note('F#2'), Note('B2'), Note('E3'))).add_notes(notes)

g.plot_all_chords(text_style='br357t', title=chord_name, use_open_string=True, highest_bass_string=1, top_note=None, lowest_soprano_string=3)
plt.savefig(f'outputs/{file_name}.svg', bbox_inches='tight')
