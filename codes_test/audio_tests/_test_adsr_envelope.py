from audio import ADSREnvelope
import matplotlib.pyplot as plt
import numpy as np

adsr = ADSREnvelope(0.1, 0.1, 0.5, 0.1)

ys0 = [next(adsr) for _ in range(20000)]
adsr.set_status(0)
ys1 = [next(adsr) for _ in range(2205)]
adsr.set_status(1)
ys2 = [next(adsr) for _ in range(6000)]
adsr.set_status(0)
ys3 = [next(adsr) for _ in range(6000)]

xs0 = np.arange(0, len(ys0))
xs1 = np.arange(len(ys0), len(ys0) + len(ys1))
xs2 = np.arange(len(ys0) + len(ys1), len(ys0) + len(ys1) + len(ys2))
xs3 = np.arange(len(ys0) + len(ys1) + len(ys2), len(ys0) + len(ys1) + len(ys2) + len(ys3))

plt.plot(xs0, ys0, 'black', xs1, ys1, 'red', xs2, ys2, 'green', xs3, ys3, 'blue')
plt.show()
