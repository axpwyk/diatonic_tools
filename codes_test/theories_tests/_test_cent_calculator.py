import matplotlib.pyplot as plt
import numpy as np
from utils_im import *


def ratio_to_cents(r):
    t = 2**(1/12)
    t_cent = t**(1/100)
    return np.log(r)/np.log(t_cent)


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

print('12-TET C Lydian cents')
for r in c_lydian_12_freqs:
    print(f'{ratio_to_cents(r):4.2f}\t', end='')
print()
print('19-TET C Lydian cents')
for r in c_lydian_19_freqs:
    print(f'{ratio_to_cents(r):4.2f}\t', end='')
print()
print('12-TET D Lydian cents')
for r in d_lydian_12_freqs:
    print(f'{ratio_to_cents(r):4.2f}\t', end='')
print()
print('19-TET D Lydian cents')
for r in d_lydian_19_freqs:
    print(f'{ratio_to_cents(r):4.2f}\t', end='')