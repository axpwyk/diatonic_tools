import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 10, 960000)

w1 = np.sin(2*np.pi*440*t)
w2 = np.sin(2*np.pi*440*1.5*t)
w3 = np.sin(2*np.pi*440*2**(7/12)*t)

fig = plt.gcf()
fig.set_figwidth(15)
fig.set_figheight(5)
ax = fig.gca()
length = 16384
# ax.plot(t[:length], w1[:length], 'r', linewidth=0.5, zorder=0)
# ax.plot(t[:length], w2[:length], 'g', linewidth=0.5, zorder=1)
# ax.plot(t[:length], (w1+w2)[:length], 'b', linewidth=1.0, zorder=2)
ax.plot(t[:length], (w1+w2)[:length], 'r', linewidth=1.0, zorder=0)
ax.plot(t[:length], (w1+w3)[:length], 'b', linewidth=1.0, zorder=1)

fig.show()
