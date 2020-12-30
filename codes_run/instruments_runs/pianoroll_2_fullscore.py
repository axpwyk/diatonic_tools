from midi import *

file = r'../../midi/fs.mid'
sheet, tpb, _ = midi2sheet(file)
pr = Pianoroll(sheet, tpb)

pr.set_intervals(pr.get_tick_range_a(), pr.get_note_range_mg(list(range(14))))
pr.draw_pianoroll(height=16)
pr.set_track_color(2, [1.0, 0.0, 0.0])
pr.set_track_color(3, [1.0, 0.9, 0.0])
pr.set_track_color(4, [0.0, 0.8, 0.3])
pr.set_track_color(5, [0.0, 0.8, 0.3])
pr.set_track_color(6, [0.0, 0.2, 0.8])
pr.set_track_color(12, [1.0, 0.4, 0.2])
pr.set_track_color(13, [1.0, 0.4, 0.2])
pr.draw_notes(list(range(14)), color_scheme='track', alpha=0.5)
pr.draw_control_changes(6, plot_type='stair_fill', alpha=0.5)
pr.show_legends()
plt.savefig('FullScore.svg')
