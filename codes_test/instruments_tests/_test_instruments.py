import os; os.chdir('../..')
from instruments import *

cs = ChordScale('D Phrygian(#3)').set_printoptions(ns=2)
ch = Chord('DbM7(#11)/Ab').set_printoptions(ns=1)

g = Guitar()
p = Piano()
c = Clock()
s = ColorScheme()
l = GenLine([Chord('FM7(9)').set_printoptions(ns=1), Chord('Em7(b13)').set_printoptions(ns=1), Chord('Dm7(b13)').set_printoptions(ns=1), Chord('C# R.4.b7.b3.b6.b2').set_printoptions(ns=0)])
t = Tonnetz()

# scale on guitar
g.set_notes(cs).plot(color_style='avoid', title=cs.get_name()[0])
plt.savefig('outputs/instrument_examples/guitar_chord_test.svg', bbox_inches='tight')

# guitar chord diagrams
g.set_notes(ch).plot_all_chords(color_style='br357t', title=ch.get_name())
plt.savefig('outputs/instrument_examples/guitar_chord_all_test.svg', bbox_inches='tight')

# scale on piano (old)
p.set_notes(cs).plot_old(color_style='avoid', title=cs.get_name()[0])
plt.savefig('outputs/instrument_examples/piano_old_scale_test.svg', bbox_inches='tight')

# chord on piano (old)
p.set_notes(ch).plot_old(color_style='br357t', title=ch.get_name())
plt.savefig('outputs/instrument_examples/piano_old_chord_test.svg', bbox_inches='tight')

# scale on piano
p.set_notes(cs).plot(color_style='degree', title=cs.get_name()[0])
plt.savefig('outputs/instrument_examples/piano_scale_test.svg', bbox_inches='tight')

# chord on piano
p.set_notes(ch).plot(color_style='br357t', title=ch.get_name())
plt.savefig('outputs/instrument_examples/piano_chord_test.svg', bbox_inches='tight')

# scale on clock
c.set_notes(cs).plot(color_style='degree', title=cs.get_name()[0])
plt.savefig('outputs/instrument_examples/clock_scale_test.svg', bbox_inches='tight')

# chord on clock
c.set_notes(ch).plot(color_style='br357t', title=ch.get_name())
plt.savefig('outputs/instrument_examples/clock_chord_test.svg', bbox_inches='tight')

# scale color scheme
s.set_notes(cs).plot(n_gradients=16, title=cs.get_name()[0])
plt.savefig('outputs/instrument_examples/color_scheme_scale_test.svg', bbox_inches='tight')

# chord color scheme
s.set_notes(ch).plot(n_gradients=16, title=ch.get_name())
plt.savefig('outputs/instrument_examples/color_scheme_chord_test.svg', bbox_inches='tight')

# chord on genline
l.plot(color_style='br357t', key_note=Note('C'), title='one_summer_day_chords')
plt.savefig('outputs/instrument_examples/gen_line_chord_test.svg', bbox_inches='tight')

# scale on tonnetz
t.set_notes(cs).plot(color_style='degree', upside_down=True, tds_on=True, title=cs.get_name()[0])
plt.savefig('outputs/instrument_examples/tonnetz_scale_test.svg', bbox_inches='tight')

# chord on tonnetz
t.set_notes(ch).plot(color_style='br357t', upside_down=True, tds_on=True, title=ch.get_name())
plt.savefig('outputs/instrument_examples/tonnetz_chord_test.svg', bbox_inches='tight')
