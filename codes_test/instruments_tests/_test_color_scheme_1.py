from instruments import *

name = 'C Ionian(b3)'
notes = AlteredDiatonicScale(name).get_notes()

cs = ColorScheme(notes)
cs.plot(name)
plt.show()
