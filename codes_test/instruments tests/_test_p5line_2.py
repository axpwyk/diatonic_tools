from instruments import *

# chord sets
chord_set_1 = ['Am', 'Em', 'F', 'C', 'Cm', 'Dm7-5', 'Ebaug7', 'G7']  # from "One Summer Day"
chord_set_2 = ['Em7(b13)', 'Dm7(b13)']

# get chords
chords = []
chord_names = []
for chord_name in chord_set_2:
    chord = Chord(chord_name)
    chords.append(chord)
    chord_names.append(chord_name)
    print(chord)

# draw perfect 5th re-arranged chord notes
p5line = P5Line(chords, chord_names)
p5line.draw()
plt.savefig('p5line.svg', dpi=300, bbox_inches='tight')
