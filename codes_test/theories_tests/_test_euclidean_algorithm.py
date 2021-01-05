def euclidean_algorithm(N, G):
    # N = q_0 * G + r_0
    if G == 1:
        return [N, ], [0, ]
    else:
        qs = [N // G]
        rs = [G, N % G]
        while rs[-1] != 1:
            qs.append(rs[-2] // rs[-1])
            rs.append(rs[-2] % rs[-1])
        return qs, rs[1:]


N = 19
G = 8
qs, rs = euclidean_algorithm(N, G)
print(qs, rs)
print(f'step: {sum(qs[:-2])}')
print([G*k%N for k in range(pow(G, -1, N))])
