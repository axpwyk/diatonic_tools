from midi import *
from pathlib import Path

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/test2.mid'))

tracks = [1]

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals(pr.get_tick_range(), pr.get_note_ranges(tracks))

pr.draw_pianoroll(height=8, aspect_note=1.2, dpi=72, type='piano')
pr.draw_notes(tracks, 'velocity', alpha=0.65, type='piano')

plt.savefig(Path(f'../output/pianoroll_test.svg'))
plt.close()
