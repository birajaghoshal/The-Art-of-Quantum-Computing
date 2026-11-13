from math import comb

n = 4
N = 2 ** n                               # 16 possible inputs
half = N // 2
print(f"n = {n}: a deterministic algorithm may need "
      f"{half + 1} queries")
print("k queries | P(balanced f looks constant)")
for k in range(2, half + 2):
    # all k distinct inputs give the same output value
    p = 2 * comb(half, k) / comb(N, k)
    print(f"{k:9d} | {p:.4f}")
