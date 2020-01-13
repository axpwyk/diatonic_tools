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


# for i in range(42):
#     t = np.linspace(0, 1, 1000)
#     b = bezier(t, np.random.rand(100, 2))
#     plt.gca(aspect='equal')
#     plt.gca().set_xticks([])
#     plt.gca().set_yticks([])
#     plt.subplots_adjust(0.1, 0.1, 0.9, 0.9)
#     plt.gcf().set_figwidth(10)
#     plt.gcf().set_figheight(10)
#     plt.plot(b[:, 0], b[:, 1], color=[i/42, 1-i/42, 1-i/42])
# plt.savefig('my_mind.svg')

# lambdas = np.linspace(0, 1, 100)
# control_points = np.random.rand(4, 2)
# bz = Bezier(lambdas, control_points)
# plot(*bz.get_control_points(0, 50), zorder=0)
# plot(*bz.get_control_points(1, 50), zorder=1)
# plot(*bz.get_control_points(2, 50), zorder=2)
# plot(*bz.get_data(), color='red', zorder=3)
# scatter(*bz.get_control_points(3, 50), zorder=4)
# plt.show()

lambdas = np.linspace(0, 1, 12000)
grids = 7
control_points = np.reshape(np.stack(np.meshgrid(np.linspace(-2, 2, grids, endpoint=True), np.linspace(-2, 2, grids, endpoint=True)), axis=-1), (-1, 2))
np.random.shuffle(control_points)
degree = 5
rotate = np.array([[np.cos(np.deg2rad(degree)), np.sin(np.deg2rad(degree))], [-np.sin(np.deg2rad(degree)), np.cos(np.deg2rad(degree))]])
control_points_rotated = np.dot(control_points, rotate)

bz = Bezier(lambdas, control_points[:, :2])
_ = [scatter(*bz.get_control_points(k, 50), color='black', zorder=0) for k in range(1)]
_ = [scatter(*control_points_rotated.T, color='red', zorder=0) for k in range(1)]
plot(*bz.get_data(), color='red', zorder=3)
_ = [plt.text(cp[0]+0.02, cp[1]+0.02, f'{k}', fontdict={'fontsize': 16}) for k, cp in enumerate(control_points)]
# scatter(*bz.get_control_points(99, 50), zorder=4)
plt.gca().set_xlim([-2.2, 2.2])
plt.gca().set_ylim([-2.2, 2.2])
plt.savefig('../../output/matplotlib/grid_bezier.svg')
plt.show()
