from instruments import *

chords = ['EM7', 'F#m7', 'G#m7', 'AM7', 'B7', 'C#m7', 'D#m7-5']

n = len(chords)
fig, axs = plt.subplots(n, 1)
fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.01, hspace=0.01)
fig.set_figheight(28); fig.set_figwidth(28)
print(axs)

for i in range(n):
    g = Guitar(Chord(chords[i]).get_notes())
    # g.select('x8aaa8')
    g.plot1(0, 12, axs[i], chords[i])

plt.savefig('test.svg', bbox_inches='tight')
plt.show()
