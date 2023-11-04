from theories import *
import matplotlib.pyplot as plt


# assign a style
plt.style.use('seaborn-pastel')
plt.rc('figure', **{'dpi': 72})

# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})

# assign a chinese-supporting font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei', 'size': 16.0})
plt.rc('axes', **{'unicode_minus': False})


radius = 0.45

notes = [(Note('Db')+k*Interval('P5')).set_vector(register=0) for k in range(12)]
notes.sort(key=lambda note: note.get_nnrel())

# BASIC NOTES
for note in notes:
    x = note.get_nnrel()
    t = plt.annotate(note.get_name(show_register=False, use_latex=True), (x, 0), va='center', ha='center')
    if x in [0, 2, 4, 5, 7, 9, 11]:
        plt.gca().add_patch(plt.Rectangle((x-1/2, 0-1/2), 1, 1, fc='white', ec='black', alpha=0.2))
        # plt.gca().add_patch(plt.Circle((x, 0), radius, fc='white', ec='black', alpha=0.2))
    else:
        plt.gca().add_patch(plt.Circle((x, 0), radius, fc='black', ec='black', alpha=0.2))

# PLOTS
def plot_r357ts(chord_name, y):
    chord_notes = Chord(chord_name)
    for note in notes:
        x = note.get_nnrel()
        itvs = [int(note - chord_note) % 12 for chord_note in chord_notes]
        # chord notes
        if 0 in itvs:
            t = plt.annotate((note - chord_notes[0]).normalize().get_r357t(), (x, 1), va='center', ha='center')
            plt.gca().add_patch(plt.Circle((x, 1), radius, fc='red', ec='red', alpha=0.2))
            continue

        # m2 avoids (except dominant 7th chord)
        if 1 in itvs and chord_notes.get_name(type_only=True) != '7':
            t = plt.annotate((note-chord_notes[0]).normalize().get_r357t(), (x, 1), va='center', ha='center')
            plt.gca().add_patch(plt.Circle((x, 1), radius, fc='black', ec='black', alpha=0.8))
            continue

        # enlarge span
        if get_span([*chord_notes, note]) > get_span(chord_notes):
            t = plt.annotate((note - chord_notes[0]).normalize().get_r357t(), (x, 1), va='center', ha='center')
            plt.gca().add_patch(plt.Circle((x, 1), radius, fc='orange', ec='orange', alpha=0.2))
            continue

        # within
        t = plt.annotate((note - chord_notes[0]).normalize().get_r357t(), (x, 1), va='center', ha='center')
        plt.gca().add_patch(plt.Circle((x, 1), radius, fc='green', ec='green', alpha=0.2))
        continue

plt.gca().set_xlim(-1, 12)
plt.gca().set_ylim(-1, 2)
plt.gca().set_aspect('equal')
plt.show()
