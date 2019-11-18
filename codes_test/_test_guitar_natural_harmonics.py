from theories import *
import matplotlib.pyplot as plt

open_strings = [Note('E1'), Note('A1'), Note('D2'), Note('G2'), Note('B2'), Note('E3')]
natural_harmonics_right = [[note, ] for note in open_strings]
natural_harmonics_left = [[note, ] for note in open_strings]
intervals_right = [Interval('P8'), Interval('P5'), Interval('P4'), Interval('M3'), Interval('m3'), Interval('m3'), Interval('M2')]
intervals_left = [Interval('P5'), Interval('P4'), Interval('M3'), Interval('m3')]
for string in natural_harmonics_right:
    for interval in intervals_right:
        string.append(string[-1] + interval)
for string in natural_harmonics_left:
    for interval in intervals_left:
        string.append(string[0] + interval)
print(natural_harmonics_right)
print(natural_harmonics_left)


plt.figure(figsize=(10, 6), dpi=144)
ax = plt.gca(aspect='equal')
ax.set_frame_on(False)
ax.set_axis_off()
ax.margins(x=0.0, y=0.0)
ax.set_xlim((0, 10))
ax.set_ylim(-0.5, 5.5)
plt.subplots_adjust(right=1.0, left=0.0, bottom=0.0, top=1.0, wspace=0.1, hspace=0.1)

plt.plot((0, 10), (0, 0), lw=1.5, color='b', zorder=-1)
plt.plot((0, 10), (1, 1), lw=1.5, color='b', zorder=-1)
plt.plot((0, 10), (2, 2), lw=1.5, color='b', zorder=-1)
plt.plot((0, 10), (3, 3), lw=1.5, color='b', zorder=-1)
plt.plot((0, 10), (4, 4), lw=1.5, color='b', zorder=-1)
plt.plot((0, 10), (5, 5), lw=1.5, color='b', zorder=-1)

def add_note_right(note, n, k):
    ax = plt.gca()
    circ = plt.Circle((10-10/n, k), 0.2, color=[0.8, 0.5, 0.5])
    ax.add_patch(circ)
    ax.annotate(note.__str__(), (10-10/n, k), ha='center', va='center', size=8, color='w')

def add_note_left(note, n, k):
    ax = plt.gca()
    circ = plt.Circle((10/n, k), 0.2, color=[0.8, 0.5, 0.5])
    ax.add_patch(circ)
    ax.annotate(note.__str__(), (10/n, k), ha='center', va='center', size=8, color='w')

for k, string in enumerate(natural_harmonics_right):
    for i, note in enumerate(string):
        add_note_right(note, i + 1, k)
for k, string in enumerate(natural_harmonics_left):
    for i, note in enumerate(string[1:]):
        add_note_left(note, i+3, k)

plt.show()
plt.close()

all_notes_right = sum(natural_harmonics_right, [])
all_notes_right.sort(key=lambda n: abs(n))
print(all_notes_right)
all_notes_left = sum(natural_harmonics_left, [])
all_notes_left.sort(key=lambda n: abs(n))
print(all_notes_left)
