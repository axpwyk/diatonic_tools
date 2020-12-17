import sys
import midi

sys.stdout = open('log3.txt', 'w')

file = r'../../midi/test.mid'
sheet, ticks_per_beat, _ =  midi.midi2sheet(file)

# for i, track in enumerate(sheet):
#    print(f'<HEAD OF TRACK {i}>')
#    for msg in track:
#        print(f'{i}:\t{msg}')
#    print(f'<END OF TRACK {i}>\n')

midi.sheet2midi(sheet, ticks_per_beat)

# sheet, ticks_per_beat, _ = midi.midi2sheet('untitled.mid')
pr = midi.Pianoroll(sheet, ticks_per_beat)
pr.use_default_intervals()
pr.set_intervals(pr.get_tick_range_m(tracks=list(range(6))), pr.get_note_range_mg(tracks=list(range(6))))
pr.draw_pianoroll(aspect_note=8)
pr.draw_notes(tracks=list(range(6)), color_scheme='track', alpha=0.7)
pr.draw_pitchwheels(tracks=[2], plot_type='stair_fill', alpha=0.5)
pr.draw_control_changes(track=1, plot_type='stair_fill', alpha=0.3)
pr.show_legends()
midi.plt.savefig('untitled.svg')

sys.stdout.close()
