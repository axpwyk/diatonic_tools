import os; os.chdir('../..')
from instruments import *

# notes = [Note('Bb'), Note('C'), Note('D'), Note('E'), Note('F#'), Note('G#')]
# notes = [Note('Bb'), Note('C'), Note('D'), Note('F#')]
# chord = Chord('Gbaug/C')
# # ads = AlteredDiatonicScale('Bb Ionian(#4, #5, b7)')
# c = Clock(chord)
#
# c.plot('Gbaug/C', 10)
# plt.show()

c = Clock().set_notes(Chord('Db(#6)'))
c.plot()
plt.show()
