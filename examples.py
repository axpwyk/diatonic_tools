from instruments import *

scale = AlteredDiatonicScale('D Phrygian(#3)')
chord = Chord('FM7(#11)/D')

g = Guitar()
p = Piano()
c = Clock()
cs = ColorScheme()
t = Tonnetz()

# scale on guitar
g.set_notes(scale).plot(color_style='degree')
plt.show()

# chord on guitar
g.set_notes(chord).plot(color_style='br357t')
plt.show()

# guitar chord diagrams
g.set_notes(chord).plot_all_chords(color_style='br357t')
plt.show()

# scale on piano (old)
p.set_notes(scale).plot_old(color_style='degree')
plt.show()

# chord on piano (old)
p.set_notes(chord).plot_old(color_style='br357t')
plt.show()

# scale on piano
p.set_notes(scale).plot(color_style='degree')
plt.show()

# chord on piano
p.set_notes(chord).plot(color_style='br357t')
plt.show()

# scale on clock
c.set_notes(scale).plot(color_style='degree')
plt.show()

# chord on clock
c.set_notes(chord).plot(color_style='br357t')
plt.show()

# scale color scheme
cs.set_notes(scale).plot()
plt.show()

# chord color scheme
cs.set_notes(chord).plot()
plt.show()

# scale on tonnetz
t.set_notes(scale).plot(color_style='degree')
plt.show()

# chord on tonnetz
t.set_notes(chord).plot(color_style='br357t')
plt.show()
