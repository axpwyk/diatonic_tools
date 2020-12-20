from instruments import *

# get chords
chords = []
chord_names = []
for key in CHORD_TYPE_TO_SCALE_TYPE.keys():
    chord_name = 'C' + key
    chord = Chord(chord_name)
    chords.append(chord)
    chord_names.append(chord_name)

# additional chords
chords.append(Chord('Cm7(9, 11, 13)'))
chord_names.append('*Cm7(9, 11, 13)')

chords.append(ChordEx().set_notes(bass=[], notes=[Note('C'), Note('Eb'), Note('Ab'), Note('Bb')]))
chord_names.append('*Cm7+5(enharmonic) = Abadd9')

chords.append(Chord('Em7(b13)'))
chord_names.append('*Em7(b13)')

chords.append(Chord('D7(11)'))
chord_names.append('*D7(11)')

# draw perfect 5th re-arranged chord notes
p5line = P5Line(chords, chord_names)
p5line.plot()
plt.savefig('p5line.svg', dpi=300, bbox_inches='tight')
