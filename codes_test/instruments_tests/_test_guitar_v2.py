from theories import Chord
from instruments import Guitar, GuitarV2, plt

g = GuitarV2(max_span=4).set_notes(Chord('E 6(9)'))
g.plot_all_chords(color_style='br357t')
plt.show()
