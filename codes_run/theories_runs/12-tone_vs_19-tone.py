import matplotlib.pyplot as plt
import numpy as np
from utils_im import *

c_lydian_12 = [7*k%12 for k in range(7)]
d_lydian_12 = [(2+7*k)%12 for k in range(7)]
c_lydian_19 = [11*k%19 for k in range(7)]
d_lydian_19 = [(3+11*k)%19 for k in range(7)]

c_lydian_12.sort()
d_lydian_12.sort()
d_lydian_12.append(d_lydian_12.pop(0)+12)
c_lydian_19.sort()
d_lydian_19.sort()
d_lydian_19.append(d_lydian_19.pop(0)+19)

c_lydian_12_freqs = [pow(2, i/12) for i in c_lydian_12]
d_lydian_12_freqs = [pow(2, i/12) for i in d_lydian_12]
c_lydian_19_freqs = [pow(2, i/19) for i in c_lydian_19]
d_lydian_19_freqs = [pow(2, i/19) for i in d_lydian_19]

fig, axs = plt.subplots(1, 2)

axs[0].plot_old(c_lydian_12, c_lydian_12_freqs, 'r*', c_lydian_12, c_lydian_19_freqs, 'b--')
axs[0].set_xticks(c_lydian_12)
axs[0].set_xticklabels(['$C$', '$D$', '$E$', '$F\sharp$', '$G$', '$A$', '$B$'])
axs[0].set_ylim([0.9, 2.2])
axs[0].grid()
axs[0].legend(['12-TET C Lydian frequencies', '19-TET C Lydian frequencies'])

axs[1].plot_old(d_lydian_12, d_lydian_12_freqs, 'r*', d_lydian_12, d_lydian_19_freqs, 'b--')
axs[1].set_xticks(d_lydian_12)
axs[1].set_xticklabels(['$D$', '$E$', '$F\sharp$', '$G\sharp$', '$A$', '$B$', '$C\sharp$'])
axs[1].set_ylim([0.9, 2.2])
axs[1].grid()
axs[1].legend(['12-TET D Lydian frequencies', '19-TET D Lydian frequencies'])

fig.set_figwidth(12)

plt.savefig(f'12_vs_19.svg', bbox_inches='tight')
