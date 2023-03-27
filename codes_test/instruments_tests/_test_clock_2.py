from utils_im import *

# ----- para ----- #

R = 5
N = 13
G = 8
M = pow(G, -1, N)
step = np.exp(-1j * 2 * np.pi / N)
init_rotation = np.exp(1j * np.pi / 2)

# ---- face ----- #

points = np.array([R * init_rotation * (step ** i) for i in range(N)])
xs = points.real
ys = points.imag

# ----- data ----- #

notes_gen = [i * G for i in range(M)]
notes_gen_points = np.array([R * init_rotation * (step ** i) for i in notes_gen])
notes_xs = (notes_gen_points).real
notes_ys = (notes_gen_points).imag

notes_color_coding = [(i * G) // N for i in range(M)]
n_colors = max(notes_color_coding) + 1
lin_color_space = [hsv_to_rgb(i, 0.5, 0.8) for i in np.linspace(0, 1, n_colors, endpoint=False)]
notes_color = [lin_color_space[i] for i in notes_color_coding]

# ----- draw ----- #

# figure settings
fig, ax = add_figure_2d(10, 10, 'image')
ax.set_xlim([-R-1, R+1])
ax.set_ylim([-R-1, R+1])

# clock face
ax.add_patch(plt.Circle((0, 0), R, fc='none', ec='black'))
for i, (x, y) in enumerate(zip(xs, ys)):
    plt.plot((0.98*x, x), (0.98*y, y), color='black')
    plt.annotate(f'{i}', (0.9*x, 0.9*y), color='black', ha='center', va='center')

# clock hands and texts
for i, (x, y) in enumerate(zip(notes_xs, notes_ys)):
    plt.plot((0, 0.8*x), (0, 0.8*y), color=notes_color[i])
    plt.annotate(f'{i}', (1.1*x, 1.1*y), color=notes_color[i], ha='center', va='center')

savefig(f'clock_N{N}_G{G}_M{M}.svg')
