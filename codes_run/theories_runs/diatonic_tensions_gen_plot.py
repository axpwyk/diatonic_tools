from theories import *
from utils_im import *

radius = 0.45
notes = [(Note('Gb')+k*Interval('P5')).set_vector(register=0) for k in range(2*N-M)]
offset_bottom = -7
offset_top = 3
notes_ex = [(Note('Gb')+k*Interval('P5')).set_vector(register=0) for k in range(offset_bottom, 2*N-M+offset_top)]

# BASIC NOTES
def draw_basic_notes(ax):
    for note in notes:
        x = note.get_gidx()
        t = ax.annotate(note.get_name(show_register=False, use_latex=True), (x, 0), va='center', ha='center')
        if x in range(M):
            ax.add_patch(plt.Rectangle((x-radius, -radius), radius*2, radius*2, fc='white', ec='black', alpha=0.2))
        else:
            ax.add_patch(plt.Circle((x, 0), radius, fc='white', ec='black', alpha=0.2))

# PLOTS
def plot_r357ts(chord_name, y, ax):
    chord_notes = Chord(chord_name)
    for note in notes:
        x = note.get_gidx()
        itvs = [int(note - chord_note) % N for chord_note in chord_notes]
        t = ax.annotate(note.get_name(show_register=False, use_latex=True), (x + radius, y + radius), color='blue', va='top', ha='right', alpha=0.5)
        # chord notes // [T0], red
        if 0 in itvs:
            t = ax.annotate((note - chord_notes[0]).normalize().get_r357t(use_latex=True), (x, y), va='center', ha='center')
            if x - chord_notes[0].get_gidx() in range(M):
                ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2, fc='red', ec='red', alpha=0.2))
            else:
                ax.add_patch(plt.Circle((x, y), radius, fc='red', ec='red', alpha=0.2))
            continue

        # from the most unacceptable to the most acceptable

        # m2 above avoids (except dominant 7th chord, minor chord R, P5) // [T5], black
        if1 = 1 in itvs
        if2 = get_span(chord_notes, enharmonic=True) < M - 1
        if3 = 'm3' in [(chord_note - chord_notes[0]).normalize() for chord_note in chord_notes]
        if4 = (int(note - chord_notes[0]) - 1) % N not in [0, G]
        if all([if1, if2, not if3 or (if3 and if4)]):
            t = ax.annotate((note-chord_notes[0]).normalize().get_r357t(use_latex=True), (x, y), va='center', ha='center')
            if x - chord_notes[0].get_gidx() in range(M):
                ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2, fc='black', ec='black', alpha=0.8))
            else:
                ax.add_patch(plt.Circle((x, y), radius, fc='black', ec='black', alpha=0.8))
            continue

        # natural and altered at same time // [T4], gray
        if note.get_named_nnrel() in [chord_note.get_named_nnrel() for chord_note in chord_notes]:
            t = ax.annotate((note - chord_notes[0]).normalize().get_r357t(use_latex=True), (x, y), va='center', ha='center')
            if x - chord_notes[0].get_gidx() in range(M):
                ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2, fc='black', ec='black', alpha=0.2))
            else:
                ax.add_patch(plt.Circle((x, y), radius, fc='black', ec='black', alpha=0.2))
            continue

        # m2 above minor chord R, P5 // [T3], blue
        if ('m3' in [(chord_note - chord_notes[0]).normalize() for chord_note in chord_notes]) and ((int(note - chord_notes[0]) - 1) % N in [0, G]):
            t = ax.annotate((note - chord_notes[0]).normalize().get_r357t(use_latex=True), (x, y), va='center', ha='center')
            if x - chord_notes[0].get_gidx() in range(M):
                ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2, fc='blue', ec='blue', alpha=0.2))
            else:
                ax.add_patch(plt.Circle((x, y), radius, fc='blue', ec='blue', alpha=0.2))
            continue

        # enlarge span // [T2], orange
        if get_span([*chord_notes, note], enharmonic=True) > get_span(chord_notes, enharmonic=True):
            t = ax.annotate((note - chord_notes[0]).normalize().get_r357t(use_latex=True), (x, y), va='center', ha='center')
            if x - chord_notes[0].get_gidx() in range(M):
                ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2, fc='orange', ec='orange', alpha=0.2))
            else:
                ax.add_patch(plt.Circle((x, y), radius, fc='orange', ec='orange', alpha=0.2))
            continue

        # available // [T1], green
        t = ax.annotate((note - chord_notes[0]).normalize().get_r357t(use_latex=True), (x, y), va='center', ha='center')
        if x - chord_notes[0].get_gidx() in range(M):
            ax.add_patch(plt.Rectangle((x-radius, y-radius), radius*2, radius*2, fc='green', ec='green', alpha=0.2))
        else:
            ax.add_patch(plt.Circle((x, y), radius, fc='green', ec='green', alpha=0.2))
        continue

for j, quality in enumerate(['aug4', '4', 'm4', 'dim4', 'augM7sus4', 'M7sus4', 'sus4',
                             'augM7', 'aug7', 'aug', 'M7', '7', '6', '', 'M7-5', '7-5',
                             'm7+5', 'mM7', 'm7', 'm6', 'm', 'mM7-5', 'm7-5', 'dim7', 'dim',
                             'M7sus2', '7sus2', '7-5sus2', '6-5sus2', 'sus2']):
    fig_name = f'{quality if quality else "maj"}'
    fig, ax = add_figure_2d(24, 24, title=fig_name)

    draw_basic_notes(ax)
    for i, note in enumerate(notes_ex):
        plot_r357ts(f'{note.get_name(show_register=False)} {quality}', i+1, ax)

    ax.set_xlim(-6, 12)
    ax.set_ylim(-1, 18+offset_top-offset_bottom)
    ax.plot((-0.5, -0.5, 6.5, 6.5, -0.5), (-0.5, 17.5+offset_top-offset_bottom, 17.5+offset_top-offset_bottom, -0.5, -0.5), 'b')
    ax.set_aspect('equal')
    savefig(f'dt_{j}_{fig_name}.pdf')
    plt.close(fig)

'''
红色：和弦内音
黑色：和弦内音上方小二度（跨度大于等于属七和弦除外，小和弦主音属音上方小二度除外）
灰色：自然音和变化音同时存在
蓝色：小和弦主音属音上方小二度
橙色：可用 tension，但会扩大和弦整体跨度
绿色：可用 tension，不会扩大和弦整体跨度
'''