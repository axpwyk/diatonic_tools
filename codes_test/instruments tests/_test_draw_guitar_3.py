from instruments import *

chords = ['G7(13)', 'Db7(#9)']

n = len(chords)
fig, axs = plt.subplots(n, 1)
fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.01, hspace=0.01)
fig.set_figheight(28); fig.set_figwidth(28)
print(axs)

for i in range(n):
    g = Guitar(Chord(chords[i]).get_notes())
    # g.select('x8aaa8')
    g.plot2(0, 12, axs[i], chords[i])

plt.savefig('test_guitar_plot.svg', bbox_inches='tight')
plt.show()
a