from midi import *
from time import gmtime, strftime

sheet, ticks_per_beat, _ = midi2sheet(Path(r'../midi/nightingale_variation.mid'))

tracks = [11]

pr = Pianoroll(sheet, ticks_per_beat)
pr.set_intervals(time_interval=(1920, pr.get_tick_range_a()[1]))
pr.set_intervals(note_interval=pr.get_note_range_ml(tracks))

pr.draw_pianoroll(height=8, aspect_note=4, dpi=72, type='piano')
pr.draw_notes(tracks, 'velocity', alpha=1.0, type='lyric')

set_tempos = pr.get_set_tempos()
mspt = [st[1]/ticks_per_beat for st in set_tempos][0]
timeline_x = list(range(0, pr.get_tick_range_a()[1]//1920*1920+1920, 1920))
timeline_s = [strftime('%H:%M:%S', gmtime((tx-1920)*mspt/1000000)) for tx in timeline_x]
timeline_s[27] = timeline_s[27]+' (A1)'
timeline_s[51] = timeline_s[51]+' (B1)'
timeline_s[59] = timeline_s[59]+' (B1\')'
timeline_s[68] = timeline_s[68]+' (C1)'
timeline_s[100] = timeline_s[100]+' (A2)'
timeline_s[148] = timeline_s[148]+' (C2)'

pr.show_chords(timeline_x, timeline_s)

pr.save(f'../output/pianoroll_test.svg')
