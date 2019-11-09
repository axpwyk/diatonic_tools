from midi import *

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/ng.mid'))

tracks = [1]
lyric = 'くものなかからおちるあめのみずむさべつなかさにげきついする'

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals(time_interval=(0*1920, 4*1920))
pr.set_intervals(note_interval=pr.get_local_note_ranges(tracks))

pr.draw_pianoroll(height=8, aspect_note=3, dpi=72, type='piano')
pr.draw_notes(tracks, 'track', alpha=0.85, type='piano', lyric=lyric)
pr.draw_notes([2, 3], 'track', alpha=0.85, type='piano', lyric=None)
pr.draw_pitchwheels(tracks, alpha=0.85)
pr.draw_pitchwheels([2, 3], alpha=0.85)
pr.draw_control_changes(1, (64, ), alpha=0.85)
pr.show_legends()
pr.show_chords([0*1920, 2*1920, 3*1920-240], ['Bm', 'G6', 'F#m7'])
pr.save(f'../output/pianoroll_test.svg')
