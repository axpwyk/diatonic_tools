import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.transforms import ScaledTranslation

fig, ax = plt.subplots()

xdata, ydata = (0.2, 0.7), (0.5, 0.5)
ax.plot(xdata, ydata, "o")
ax.set_xlim((-2, 2))
ax.set_ylim((-2, 2))
trans = (fig.dpi_scale_trans +
         ScaledTranslation(xdata[0], ydata[0], ax.transData))

# plot an ellipse around the point that is 150 x 130 points in diameter...
circle = Ellipse((0, 0), 2, 1, angle=45,
                          fill=None)#, transform=trans)
ax.add_patch(circle)
plt.show()
