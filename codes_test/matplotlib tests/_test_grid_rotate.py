from movie import *


def _settings():
    plt.gcf().set_figwidth(10)
    plt.gcf().set_figheight(10)
    plt.subplots_adjust(0.1, 0.1, 0.9, 0.9)
    plt.gca(aspect='equal')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])


def plot(*args, **kwargs):
    if not plt.fignum_exists(1):
        _settings()
    plt.plot(*args, **kwargs)


def scatter(*args, **kwargs):
    if not plt.fignum_exists(1):
        _settings()
    plt.scatter(*args, **kwargs)


grids = 16
control_points = np.reshape(np.stack(np.meshgrid(np.linspace(-2, 2, grids, endpoint=True), np.linspace(-2, 2, grids, endpoint=True)), axis=-1), (-1, 2))
#np.random.shuffle(control_points)
degree = 95
rotate = np.array([[np.cos(np.deg2rad(degree)), np.sin(np.deg2rad(degree))], [-np.sin(np.deg2rad(degree)), np.cos(np.deg2rad(degree))]])
control_points_rotated = np.dot(control_points, rotate)

plot(*control_points.T, color='black', zorder=-1, lw=1)
plot(*control_points_rotated.T, color='red', zorder=-1, lw=1)
scatter(*control_points.T, color='black', zorder=0)
scatter(*control_points_rotated.T, color='red', zorder=0)

plt.gca().set_xlim([-2.5, 2.5])
plt.gca().set_ylim([-2.5, 2.5])
plt.savefig('../../output/matplotlib/grid_bezier.svg')
plt.show()
