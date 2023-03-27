from utils_im import *

# ----- para ----- #

N = 13
G = 8
S = 0
M = pow(G, -1, N)
step = 1
M2 = M - (N % M)

# ---- face ----- #

points = np.array([step * i for i in range(N)])

# ----- data ----- #

notes_gen = [(S + i * G) % N for i in range(M)]
notes_gen_points = np.array([step * i for i in notes_gen])

notes_color_coding = [(S + i * G) // N for i in range(M)]
n_colors = max(notes_color_coding) + 1
lin_color_space = [hsv_to_rgb(i, 0.5, 0.8) for i in np.linspace(0, 1, n_colors, endpoint=False)]
notes_color = [lin_color_space[i] for i in notes_color_coding]

# ----- draw ----- #

# figure settings
fig, ax = add_figure_2d(N, 10, 'image')
ax.set_xlim([-1, (N * step).real + 1])
ax.set_ylim([-1, n_colors + 0.5])

# face
for i, x in enumerate(points):
    ax.plot((x, x+step), (0, 0), color='black')
    ax.plot((x, x), (0, 0.1), color='black')
    ax.plot((x+step, x+step), (0, 0.1), color='black')
    ax.annotate(f'{i}', (x, -0.5), color='black', ha='center', va='center')

# hands and texts
for i, x in enumerate(notes_gen_points):
    ax.annotate(f'{i}$\\times$', (x, notes_color_coding[i]+1-0.25), color=notes_color[i], ha='center', va='center')
    # ax.add_patch(plt.Circle((x, notes_color_coding[i]+1-0.25), radius=0.2, ec=notes_color[i], fc='none'))
    ax.plot((x, x), (notes_color_coding[i]+1-0.25-0.2, 0.1), ':', color=notes_color[i])

savefig(f'linline_N{N}_G{G}_S{S}_M{M}_M2-{M2}.pdf')
