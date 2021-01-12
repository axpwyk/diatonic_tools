from instruments import *

# # guitar
# Guitar().set_notes(Chord('Caug/F#')).plot(title='Caug/F# (color_style=note)')
# plt.savefig('../../outputs/instrument_examples/guitar_Caug_on_F_sharp_note.svg', bbox_inches='tight')
#
# Guitar().set_notes(Chord('Caug/F#')).plot(color_style='br357t', title='Caug/F# (color_style=br357t)')
# plt.savefig('../../outputs/instrument_examples/guitar_Caug_on_F_sharp_br357t.svg', bbox_inches='tight')
#
# Guitar().set_notes(Chord('C')).plot(fret_left=0, fret_right=4, selection='x32010', color_style='br357t', title='C (color_style=br357t)')
# plt.savefig('../../outputs/instrument_examples/guitar_C_br357t.svg', bbox_inches='tight')
#
# Guitar().set_notes(AlteredDiatonicScale('C Phrygian(#3)')).plot(color_style='degree', title='C Phrygian(#3) (color_style=degree)')
# plt.savefig('../../outputs/instrument_examples/guitar_C_Phrygian_Dominant_degree.svg', bbox_inches='tight')
#
# Guitar().set_notes(Chord('Caug/F#')).plot_all_chords(color_style='br357t', title='Caug/F# (color_style=br357t)')
# plt.savefig('../../outputs/instrument_examples/guitar_Caug_on_F_sharp_all_br357t.svg', bbox_inches='tight')
#
# Guitar(open_string_notes=(Note('C#1'), Note('G#1'), Note('E2'), Note('F#2'), Note('B2'), Note('E3'))).add_notes(Chord('Esus2/G#')).plot_all_chords(color_style='br357t', title='Esus2/G# (color_style=br357t)')
# plt.savefig('../../outputs/instrument_examples/guitar_Esus2_on_G_sharp_all_br357t.svg', bbox_inches='tight')
#
# # piano
# Piano().set_notes(ChordScale('C Dorian(b4)')).plot_old(color_style='avoid', title='C Dorian(b4) (color_style=avoid)')
# plt.savefig('../../outputs/instrument_examples/piano_old_C_Dorian(b4)_avoid.svg', bbox_inches='tight')
#
# Piano().set_notes(ChordScale('C Mixolydian(b2)')).plot(color_style='avoid', title='C Dorian(b4) (color_style=avoid)')
# plt.savefig('../../outputs/instrument_examples/piano_C_Mixolydian(b2)_avoid.svg', bbox_inches='tight')
#
# # clock
# Clock().set_notes(AlteredDiatonicScale('D Lydian(b7)')).plot(color_style='degree', interval_anno_style='interval', title='D Lydian(b7)', subtitle='color_style=degree')
# plt.savefig('../../outputs/instrument_examples/clock_D_Lydian(b7)_degree.svg', bbox_inches='tight')
#
# # color scheme
# ColorScheme().set_notes(Chord('Daug')).plot(n_gradients=5, title='Daug (Triadic Color Scheme)')
# plt.savefig('../../outputs/instrument_examples/color_scheme_Daug.svg', bbox_inches='tight')
#
# # gen line
# GenLine([Chord('FM7(9)').set_printoptions(ns=1), Chord('Em7(b13)').set_printoptions(ns=1), Chord('Dm7(b13)').set_printoptions(ns=1), Chord('C# R.4.b7.b3.b6.b2')]).plot(color_style='br357t', key_note=Note('C'), tds_on=True, title='One Summer Day Chords (color_style=br357t)')
# plt.savefig('../../outputs/instrument_examples/gen_line_one_summer_day_chords_br357t.svg', bbox_inches='tight')
#
# # tonnetz
# Tonnetz().set_notes(Chord('Cm7')).plot(color_style='br357t', title='Cm7 (color_style=br357t)')
# plt.savefig('../../outputs/instrument_examples/tonnetz_Cm7_br357t.svg', bbox_inches='tight')

# 19-TET
Piano().set_notes(DiatonicScale('C Ionian')).plot(title='C Ionian (19-TET)')
plt.savefig('../../outputs/instrument_examples/19-TET_piano_C_Ionian_note.svg', bbox_inches='tight')
