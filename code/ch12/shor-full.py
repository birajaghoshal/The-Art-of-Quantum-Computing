# The whole of Shor's algorithm for N = 15: classical shell,
# quantum order finding (one shot per attempt), classical finish
import random
import numpy as np
from math import gcd
from qiskit.primitives import StatevectorSampler
from shorlib import order_finding, guess_order, factors_from_order

N, t = 15, 8
random.seed(7)
# a Generator (not an int): each one-shot run gets fresh randomness
sampler = StatevectorSampler(seed=np.random.default_rng(3))
for attempt in range(1, 11):
    a = random.randrange(2, N)
    if gcd(a, N) > 1:                   # rare lucky guess
        print(f"attempt {attempt}: a = {a} shares "
              f"{gcd(a, N)} with N")
        break
    qc = order_finding(a, N, t)
    res = sampler.run([qc], shots=1).result()[0].data.c
    k = int(next(iter(res.get_counts())), 2)
    r = guess_order(k, t, a, N)
    f = factors_from_order(a, r, N)
    print(f"attempt {attempt}: a = {a:>2}, k = {k:>3}, r = {r}, "
          f"factors = {f}")
    if f:
        break
