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

lambdas = np.linspace(0, 1, 100)
control_points = np.random.rand(4, 2)
bezier = Bezier(lambdas, control_points)

plot(*bezier.get_control_points(0, 50), zorder=0)
plot(*bezier.get_control_points(1, 50), zorder=1)
plot(*bezier.get_control_points(2, 50), zorder=2)
plot(*bezier.get_data(), color='red', zorder=3)
scatter(*bezier.get_control_points(3, 50), zorder=4)
plt.show()
