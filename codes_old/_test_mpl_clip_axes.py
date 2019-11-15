import matplotlib.pyplot as plt

circ = plt.Circle((0, 0), 1.2)
plt.gca().add_patch(circ)
plt.gca().set_xlim((-1, 1))
plt.gca().set_ylim((-1, 1))

plt.savefig(r'../output/axes_clip.svg')
plt.show()
plt.close()
