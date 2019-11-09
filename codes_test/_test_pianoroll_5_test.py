from midi import *

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/test2.mid'))

tracks = [1]
# lyric = 'くものなかからおちるあめのみずむさべつなかさにげきついする'
lyric = []

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals(time_interval=(2*1920, pr.get_max_tick()))
pr.set_intervals(note_interval=pr.get_local_note_ranges(tracks))

pr.draw_pianoroll(height=6, aspect_note=2, dpi=72, type='piano')
pr.draw_notes(tracks, 'velocity', alpha=0.85, type='piano', lyric=lyric)
pr.draw_pitchwheels(tracks, alpha=0.85)
pr.draw_control_changes(1, (64, ), alpha=0.85)
pr.show_legends()
pr.show_chords([2*1920, 4*1920, 5*1920-240, 6*1920, 8*1920, 9*1920-240], ['Cm', 'Ab6', 'Gm7']*2)
pr.save(f'../output/pianoroll_test.svg')
