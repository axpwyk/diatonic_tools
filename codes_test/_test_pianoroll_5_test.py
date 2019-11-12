from midi import *

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/cyberpunk.mid'))

tracks = [21]

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals(time_interval=(12*1920, 19*1920))
pr.set_intervals(note_interval=pr.get_note_range_ml(tracks))

pr.draw_pianoroll(height=8, aspect_note=4, dpi=72, type='piano')
pr.draw_notes(tracks, 'velocity', alpha=1.0, type='lyric')
pr.draw_pitchwheels(tracks, alpha=1.0)
pr.draw_control_changes(tracks[0], pr.get_used_controls(tracks[0]), alpha=1.0)
pr.show_legends()

pr.save(f'../output/pianoroll_test.svg')
