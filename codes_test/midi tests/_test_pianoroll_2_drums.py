from midi import *
from pathlib import Path

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/drum_funk.mid'))

tracks = [1]

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals((0*1920, 4*1920), (35, 57))

pr.draw_pianoroll(height=8, aspect_note=4, dpi=72, type='drum')
pr.draw_notes(tracks, 'velocity', alpha=0.65, type='drum')

plt.savefig(Path(f'../output/pianoroll_test.svg'))
plt.close()
