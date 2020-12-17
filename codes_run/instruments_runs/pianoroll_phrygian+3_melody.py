import midi

sheet, tpb, tt = midi.midi2sheet(r'../midi/phrygian+3_melody.mid')
pr = midi.Pianoroll(sheet, tpb)

pr.set_intervals(pr.get_tick_range_a(), pr.get_note_range_mg([0]))
pr.draw_pianoroll(aspect_note=4)
pr.draw_notes(tracks=[0], color_scheme='track', alpha=1)
midi.plt.savefig(r'../output/phrygian+3_melody.svg')
