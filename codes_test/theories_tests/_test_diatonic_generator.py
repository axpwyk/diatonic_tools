from copy import copy, deepcopy

N = 21
L = 5
M = pow(L, -1, N)

a1 = [L*k for k in range(M)]
a2 = [k%N for k in a1]
a3 = copy(a2); a3.sort()

print(f'a1: {a1}')
print(f'a2: {a2}')
print(f'a3: {a3}')
