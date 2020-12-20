from instruments import *

chords = ['E7(#9)']

n = len(chords)
fig, axs = plt.subplots(n, 1)
fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.01, hspace=0.01)
fig.set_figheight(4); fig.set_figwidth(4)
print(axs)

g = Guitar(Chord(chords[0]).get_notes())
# g.select('xxxxxx')
g.plot2(0, 12, axs, chords)

# for i in range(n):
#     g = Guitar(Chord(chords[i]).get_notes())
#     g.select('x13131')
#     g.plot2(0, 12, axs[i], chords[i])

plt.savefig('test_guitar_plot.svg', bbox_inches='tight')
plt.show()
