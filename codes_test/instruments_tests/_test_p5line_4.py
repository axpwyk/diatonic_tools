from instruments import *

chords = []
chord_names = []

# additional chords
chords.append(Chord('Csus2/E'))
chord_names.append('Csus2/E')

chords.append(Chord('E7-5'))
chord_names.append('E7-5')

chords.append(Chord('FM7'))
chord_names.append('FM7')

chords.append(Chord('Gm(11, 13)'))
chord_names.append('Gm(11, 13)')

chords.append(Chord('Db7'))
chord_names.append('Db7')

chords.append(Chord('CM7'))
chord_names.append('CM7')

# draw perfect 5th re-arranged chord notes
p5line = P5Line(chords, chord_names)
p5line.plot()
plt.savefig('p5line.svg', dpi=300, bbox_inches='tight')
