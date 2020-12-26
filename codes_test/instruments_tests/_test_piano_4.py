import instruments as inst
from theories import *

notes = [Note('G1').set_message(br357t='R'), Note('B1').set_message(br357t='R'), Note('F2').set_message(br357t='R'), Note('Ab2'), Note('Db3'), Note('Gb3')]
inst.PianoSpecial(notes).plot(title='$\mathrm{A}\\flat 4^2/\mathrm{G}7$')

# notes = [Note('A1').set_message('B'), Note('C#2').set_message('B'), Note('G2').set_message('B'), Note('D3'), Note('F#3')]
# inst.Piano(notes).plot(title='$\mathrm{A}7(11, 13)$')

# notes = [Note('A1').set_message('B'), Note('C#2').set_message('B'), Note('G2').set_message('B'), Note('C3'), Note('E3')]
# inst.Piano(notes).plot(title='$\mathrm{A}7(\sharp9)$')

inst.plt.savefig('test_piano_plot.svg', bbox_inches='tight', pad_inches=0.0)
