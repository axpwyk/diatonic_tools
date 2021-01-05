import os; os.chdir('../..')
from theories import *
from utils_im import *

central_note = Note('C')
r = 5

top_line = [central_note+k*Interval('m3') for k in range(-r, r+1)]
all_line = [[note+k*Interval('P4') for note in top_line] for k in range(-r, r+1)]
chord_name = 'Cm(11)'
chord_notes = [k%12 for k in abs(Chord(chord_name))]

for ax0 in all_line:
    for note in ax0:
        if abs(note)%3==0:
            note.set_message(function='T')
        elif abs(note)%3==1:
            note.set_message(function='D')
        else:
            note.set_message(function='S')
        if abs(note)%12 in chord_notes:
            note.set_message(chord_note='yes')
        else:
            note.set_message(chord_note='no')

n_lines = len(all_line)
color_mapping = {'T': '#D5E8D4', 'D': '#F8CECC', 'S': '#FFF2CC'}
additional_color_mapping = {'yes': 'red', 'no': 'black'}
width, height = 2, 2

patches = [
    [
        plt.Rectangle(
            xy=(i*width, (n_lines-1-j)*height),
            width=width,
            height=height,
            facecolor=color_mapping[note.get_message('function')],
            edgecolor='black'
        )
        for i, note in enumerate(axis0)
    ]
    for j, axis0 in enumerate(all_line)
]

fig, ax = plt.subplots(1, 1)
fig.set_figwidth(8)
fig.set_figheight(8)
ax.set_xlim(0-0.1, (2*r+1)*width+0.1)
ax.set_ylim(0-0.1, (2*r+1)*height+0.1)
ax.set_axis_off()
ax.set_aspect('equal')
ax.set_title(chord_name)

for i, axis0 in enumerate(patches):
    for j, patch in enumerate(axis0):
        ax.add_patch(patch)
        bbox_props = dict(boxstyle='round', facecolor=additional_color_mapping[all_line[j][i].get_message('chord_note')], alpha=0.5)
        ax.annotate(all_line[j][i].get_name_old(show_register=False), ((i + 1 / 2) * width, (n_lines - 1 - j + 1 / 2) * height),
                    ha='center', va='center', color='white', bbox=bbox_props)

savefig(f'outputs/m3_P5_analysis_{chord_name}.svg')
