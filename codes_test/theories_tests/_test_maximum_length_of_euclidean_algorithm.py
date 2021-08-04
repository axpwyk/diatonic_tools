def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
    return a


G = fib(14)
N = fib(15)
M = pow(G, -1, N)
print(f'G, N, M = {G}, {N}, {M}')
print()


a = [(i * G) % N for i in range(M)]

print(a[0], end='\t')
for prev, next in zip(a[:-1], a[1:]):
    if prev > next:
        print()
    print(next, end='\t')
print()
print()


L = a.index(min(a[1:]))
print(L, [a[k*L%M] for k in range(M)])
