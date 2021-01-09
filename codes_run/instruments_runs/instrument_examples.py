import os; os.chdir('../..')
from instruments import *

scale = AlteredDiatonicScale('D Phrygian(#3)')
chord = Chord('Cb/Eb')

g = Guitar()
p = Piano()
c = Clock()
cs = ColorScheme()
t = Tonnetz()

# scale on guitar
g.set_notes(scale).plot(color_style='degree', title='title_test')
plt.savefig('outputs/instrument_examples/guitar_scale_test.svg', bbox_inches='tight')

# chord on guitar
g.set_notes(chord).plot(color_style='br357t', title='title_test')
plt.savefig('outputs/instrument_examples/guitar_chord_test.svg', bbox_inches='tight')

# guitar chord diagrams
g.set_notes(chord).plot_all_chords(color_style='br357t', title='title_test')
plt.savefig('outputs/instrument_examples/guitar_chord_all_test.svg', bbox_inches='tight')

# scale on piano (old)
p.set_notes(scale).plot_old(color_style='degree', title='title_test')
plt.savefig('outputs/instrument_examples/piano_old_scale_test.svg', bbox_inches='tight')

# chord on piano (old)
p.set_notes(chord).plot_old(color_style='br357t', title='title_test')
plt.savefig('outputs/instrument_examples/piano_old_chord_test.svg', bbox_inches='tight')

# scale on piano
p.set_notes(scale).plot(color_style='degree', title='title_test')
plt.savefig('outputs/instrument_examples/piano_scale_test.svg', bbox_inches='tight')

# chord on piano
p.set_notes(chord).plot(color_style='br357t', title='title_test')
plt.savefig('outputs/instrument_examples/piano_chord_test.svg', bbox_inches='tight')

# scale on clock
c.set_notes(scale).plot(color_style='degree', title='title_test')
plt.savefig('outputs/instrument_examples/clock_scale_test.svg', bbox_inches='tight')

# chord on clock
c.set_notes(chord).plot(color_style='br357t', title='title_test')
plt.savefig('outputs/instrument_examples/clock_chord_test.svg', bbox_inches='tight')

# scale color scheme
cs.set_notes(scale).plot(title='title_test', n_gradients=16)
plt.savefig('outputs/instrument_examples/color_scheme_scale_test.svg', bbox_inches='tight')

# chord color scheme
cs.set_notes(chord).plot(title='title_test', n_gradients=16)
plt.savefig('outputs/instrument_examples/color_scheme_chord_test.svg', bbox_inches='tight')

# scale on tonnetz
t.set_notes(scale).plot(color_style='degree', title='title_test', upside_down=True, tds_on=True)
plt.savefig('outputs/instrument_examples/tonnetz_scale_test.svg', bbox_inches='tight')

# chord on tonnetz
t.set_notes(chord).plot(color_style='br357t', title='title_test', upside_down=True, tds_on=True)
plt.savefig('outputs/instrument_examples/tonnetz_chord_test.svg', bbox_inches='tight')
