from movie import *

t = np.linspace(0, 5, 20)
X = fancy_motion(t, 0, 5, (0, 0), (1, 1), 'fast-in-out', factor=100)
print(X)

plt.plot(X[:, 0], X[:, 1], marker='o')
plt.show()
