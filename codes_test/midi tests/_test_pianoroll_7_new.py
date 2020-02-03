import midi

sheet, tpb, tt = midi.midi2sheet(r'../../midi/test3.mid')
pr = midi.Pianoroll(sheet, tpb)

pr.set_intervals(pr.get_tick_range_a(), pr.get_note_range_mg([2, 3]))
pr.draw_pianoroll(aspect_note=8)
pr.draw_notes(tracks=[2, 3], color_scheme='track', alpha=0.75)
midi.plt.savefig(r'../../output/pianoroll_test_2.svg')

print(sheet[1])
