# Searching when M is unknown: random iteration counts with a
# growing range (the strategy of Boyer, Brassard, Hoyer and Tapp)
import numpy as np
from groverlib import theory

rng = np.random.default_rng(42)
N = 1024

def search_cost(M):
    """Oracle calls used until a marked item is found."""
    calls, L = 0, 1.0
    while True:
        k = int(rng.integers(0, int(np.ceil(L))))   # random k < L
        calls += k + 1                          # +1: check result
        if rng.random() < theory(N, M, k):
            return calls
        L = min(1.2 * L, np.sqrt(N))            # grow the range

for M in (1, 4, 16, 64):
    avg = np.mean([search_cost(M) for _ in range(2000)])
    print(f"M = {M:>2}: average calls {avg:5.1f},  "
          f"sqrt(N/M) = {np.sqrt(N / M):4.1f},  "
          f"classical {(N + 1) / (M + 1):5.1f}")
