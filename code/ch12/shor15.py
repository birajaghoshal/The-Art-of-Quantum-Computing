# Order finding for a = 7, N = 15 (8 counting qubits), then the
# classical post-processing of every outcome
from fractions import Fraction
from qiskit.primitives import StatevectorSampler
from shorlib import order_finding, guess_order, factors_from_order

a, N, t = 7, 15, 8
qc = order_finding(a, N, t)
sampler = StatevectorSampler(seed=15)
counts = sampler.run([qc], shots=2000).result()[0].data.c \
    .get_counts()

good = {1: 0, 4: 0}
for bits, c in sorted(counts.items()):
    k = int(bits, 2)
    frac = Fraction(k, 2**t).limit_denominator(N)
    r1 = guess_order(k, t, a, N)               # denominator only
    r4 = guess_order(k, t, a, N, max_mult=4)   # also try 2r, 3r, 4r
    for m, r in ((1, r1), (4, r4)):
        good[m] += c if factors_from_order(a, r, N) else 0
    print(f"{bits} k = {k:>3} ({c} shots) -> {str(frac):>3}: "
          f"r = {r1}, with multiples r = {r4}")
print(f"shots giving a factor, denominator only: {good[1]}/2000")
print(f"shots giving a factor, with multiples:   {good[4]}/2000")
print("factors:", factors_from_order(a, 4, N))

