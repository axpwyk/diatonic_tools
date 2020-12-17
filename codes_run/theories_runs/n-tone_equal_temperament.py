from math import gcd
import matplotlib.pyplot as plt
import numpy as np

# for n in range(1, 101):
#     lst = []
#     for i in range(1, n):
#         if gcd(n, i) == 1:
#             if 1.49 <= 2**(i/n) < 1.51:
#                 lst.append(f'步长：{i:2d} | 音数：{pow(i, -1, n):2d} | 倍率：{2**(i/n):.4f}')
#
#     if lst:
#         for s in lst:
#             print(f'{n:3d}-tone | ', s)

''' ---------------------------------------------------------------------------------------------------- '''

# n = 7
#
# for i in range(1, n):
#     if gcd(n, i) == 1:
#         print(f'步长：{i:2d} | 音数：{pow(i, -1, n):2d} | 倍率：{2**(i/n):.4f}')

''' ---------------------------------------------------------------------------------------------------- '''

N = 41
M = 24
k = 12

ts12 = list(range(12))
ts41 = [M*t%N for t in range(k)]
ts41.sort()
fs12 = [2**(t/12) for t in ts12]
fs41 = [2**(t/N) for t in ts41]

plt.plot(fs12, 'r*', fs41, 'b--')
plt.legend(['12-tone equal temperament chromatic scale', '41-tone equal temperament diatonic 12-tone scale'])
plt.grid()
plt.xticks(list(range(12)))
plt.ylim([0.9, 2.1])
plt.savefig('12_vs_41.svg', bbox_inches='tight')

''' ---------------------------------------------------------------------------------------------------- '''

# ts41 = [24*t%41 for t in range(12)]
#
# black = np.pad(np.zeros((9, 9)), ((1, 1), (1, 1)), constant_values=0.5)
# white = np.ones((11, 11))
#
# lst = []
# for i in range(41):
#     if i in ts41:
#         lst.append(white)
#     else:
#         lst.append(black)
#
# out = np.concatenate(lst, 1)
#
# plt.imshow(out, cmap='gray')
# plt.show()




















