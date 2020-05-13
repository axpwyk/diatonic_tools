import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-pastel')

f = 5
t1 = np.linspace(0, 2*np.pi, 65536)
y1 = np.sin(2*np.pi*f*t1)
plt.plot(t1, y1, zorder=-1)

sr = 30
t2 = np.linspace(0, 2*np.pi, sr*f)
y2 = np.sin(2*np.pi*f*t2)
for t, y in zip(t2, y2):
    plt.plot((t, t), (0, y), c='red')
plt.scatter(t2, y2, c='red')
plt.plot(t2, y2, c='red', lw=0.5)
plt.show()
