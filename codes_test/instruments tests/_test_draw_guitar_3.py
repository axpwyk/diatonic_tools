from instruments import *

fig, axss = plt.subplots(1, 1)
fig.set_figheight(8); fig.set_figwidth(8)
for ax in [axss]:  # .flat:
    ax.set_aspect('equal')
    ax.plot(np.arange(11), np.arange(11))

    ax.annotate('')
    ins = ax.inset_axes([0.2, 0.1, 0.2, 0.2], aspect='equal')

    g = Guitar(Chord('F')[1:])
    g.select('x8aaa8')
    g.plot1(7, 11, ins)