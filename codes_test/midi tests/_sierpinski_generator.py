from midi import *
from theories import *
import numpy as np
import matplotlib.pyplot as plt

tpb = 240
step = tpb//4


def generate_unit_note(time, note_number, velocity_on):
    return dict(type='note', channel=0, note=note_number, velocity_on=velocity_on, velocity_off=64, lyric=None, time1=time, time2=step)


def _rule(a, b, c, code=115):
    code = '0'*(8-len(bin(code))+2)+bin(code)[2:]
    ind = eval('0b'+f'{a*1}{b*1}{c*1}')
    return eval(code[ind])


def automaton(code):
    automaton = np.zeros((64, 64), dtype=np.int)
    automaton[0, 1] = 1
    for i in range(1, 64):
        for j in range(64-2):
            automaton[i, j+1] = _rule(automaton[i-1, j], automaton[i-1, j+1], automaton[i-1, j+2], code)
    return automaton


# fig, axs = plt.subplots(16, 16)
# fig.set_dpi(144)
# fig.set_figwidth(20)
# fig.set_figheight(20)
# fig.subplots_adjust(0, 0, 1, 1, 0.1, 0.1)
# for i in range(16):
#     for j in range(16):
#         axs[i, j].imshow(automaton(i*16+j), cmap='gray', aspect='equal')
#         axs[i, j].set_axis_off()
#         axs[i, j].margins(0)
# fig.savefig('automaton.svg')

data = automaton(60)
chord = Chord('F6')
notes = [abs(note) for note in chord.get_notes()]
notes = np.array(notes)
notes = np.concatenate([notes+12*k for k in range(10)])
print(notes)

msglist = []
for j in range(1, 1+32):
    for i in range(0, 0+32):
        if data[i, j]:
            msglist.append(generate_unit_note(i*step, notes[j-1], 64))
sheet = [msglist]

sheet2midi(sheet, tpb, 'test.mid')

pr = Pianoroll(sheet, tpb)
pr.set_intervals(pr.get_tick_range_s(0), pr.get_note_range_sg(0))
pr.draw_pianoroll(aspect_note=16, type='piano')
pr.draw_notes()
plt.savefig('test.svg')
