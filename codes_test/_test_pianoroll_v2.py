from midi import *
from pathlib import Path

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/pw_and_cc.mid'))
track = 1

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals((0*1920, pr.max_tick), pr.get_note_range(track))

pr.draw_pianoroll(height=8, aspect_note=2.5, dpi=72)
pr.draw_notes(track, shader=rgb_shader)
pr.draw_pitchwheels(track, shader=lambda t: const_shader(t, [0.3, 0.7, 0.8]))
pr.draw_control_changes(track)
pr.show_legends()

plt.savefig(f'../output/pianoroll_test.svg')
plt.close()
