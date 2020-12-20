from instruments import *

chords = []
chord_names = []

# additional chords
chords.append(Chord('FM7(9)'))
chord_names.append('FM7(9)')

chords.append(Chord('Em7(b13)'))
chord_names.append('Em7(b13)')

chords.append(Chord('Dm7(b13)'))
chord_names.append('Dm7(b13)')

chords.append(ChordEx().set_notes(bass=[], notes=[Note('C#'), Note('F#'), Note('B'), Note('E'), Note('A'), Note('D')]))
chord_names.append('E4/C#4')

# draw perfect 5th re-arranged chord notes
p5line = P5Line(chords, chord_names)
p5line.plot()
plt.savefig('p5line.svg', dpi=300, bbox_inches='tight')
