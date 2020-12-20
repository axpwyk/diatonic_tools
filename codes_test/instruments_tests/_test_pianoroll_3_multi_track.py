from midi import *
from pathlib import Path

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/ng.mid'))

tracks = [1, 2]

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals(pr.get_tick_range(), pr.get_note_ranges(tracks))

pr.draw_pianoroll(height=8, aspect_note=6, dpi=72, type='piano')
pr.draw_notes(tracks, 'track', alpha=0.65, type='piano')
pr.draw_pitchwheels(tracks, alpha=0.65)

plt.savefig(Path(f'../output/pianoroll_test.svg'))
plt.close()
