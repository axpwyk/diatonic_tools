from midi import *
from pathlib import Path

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/ng.mid'))

tracks = [1]
lyric = 'くものなかからおちるあめのみずむさべつなかさにげきついする'

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals((0*1920, pr.get_max_tick()), pr.get_note_ranges([1]))

pr.draw_pianoroll(height=8, aspect_note=3, dpi=72, type='piano')
pr.draw_notes(tracks, 'velocity', alpha=0.65, type='piano', lyric=lyric)
pr.draw_pitchwheels(tracks, alpha=0.65)
pr.draw_control_changes(1, (64, ), alpha=0.65)
pr.show_legends()
pr.show_chords([0*1920, 2*1920, 3*1920-240], ['Bm', 'G6', 'F#m7'])

plt.savefig(Path(f'../output/pianoroll_test.svg'))
plt.close()
