"""Searching N unsorted items for one marked item.
Classical: check items in random order and count the queries.
Quantum (Grover, Chapter 13): about (pi/4) sqrt(N) queries."""
import math
import numpy as np

rng = np.random.default_rng(seed=7)
TRIALS = 2000

print(f"{'N':>9} {'classical avg':>14} {'(N+1)/2':>10} "
      f"{'Grover':>7}")
for k in range(2, 21, 3):
    N = 2**k
    # Checking in a random order, the marked item is equally
    # likely to sit at position 1, 2, ..., N: draw that position
    found_at = rng.integers(1, N + 1, size=TRIALS)
    grover = math.floor(math.pi / 4 * math.sqrt(N))
    print(f"{N:>9,} {found_at.mean():>14.1f} {(N + 1) / 2:>10.1f} "
          f"{grover:>7}")
