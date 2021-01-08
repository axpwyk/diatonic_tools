import os; os.chdir(r'../..')
import midi

sheet, tpb, tt = midi.midi2sheet(r'midi/wishing_chord.mid')
pr = midi.Pianoroll(sheet, tpb)

pr.set_intervals(pr.get_tick_range_a(), pr.get_note_range_mg([1]))
pr.draw_pianoroll(aspect_note=8)
pr.draw_notes(tracks=[1], color_style='track', alpha=1)
midi.plt.savefig(r'output/wishing_chord.svg')
