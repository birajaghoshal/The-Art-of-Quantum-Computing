import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=99)

def classical_queries(n, trials=300):
    """Average random distinct queries until f(x) = f(x XOR s)."""
    total = 0
    for _ in range(trials):
        s = int(rng.integers(1, 2 ** n))
        seen = set()
        for k, x in enumerate(rng.permutation(2 ** n), start=1):
            pair = min(x, x ^ s)         # x and x^s share one label
            if pair in seen:
                break
            seen.add(pair)
        total += k
    return total / trials

def quantum_queries(n):
    """Expected runs to collect n-1 independent equations."""
    return sum(1 / (1 - 2.0 ** (k - (n - 1))) for k in range(n - 1))

ns = np.arange(2, 17)
cl = [classical_queries(n) for n in ns]
qu = [quantum_queries(n) for n in ns]
for n, c, q in zip(ns, cl, qu):
    if n in (4, 16):
        print(f"n = {n:2d}: classical {c:7.1f}   quantum {q:5.2f}")

fig, ax = plt.subplots(figsize=(3.8, 2.3))
for y, sty, col, lab in [
        (cl, "o-", "#F28C28", "classical (random)"),
        (qu, "s-", "#1F5FBF", "Simon (expected)"),
        (2.0 ** (ns / 2), ":", "#5B6B7F", "$2^{n/2}$")]:
    ax.semilogy(ns, y, sty, color=col, label=lab, ms=4)
ax.set_xticks(range(2, 17, 2))
ax.set_xlabel("input bits $n$"); ax.set_ylabel("oracle queries")
ax.set_ylim(1.5, 3e3)
ax.legend(loc="upper left", labelspacing=0.3)
fig.tight_layout()
fig.savefig("figures/ch10/simon_scaling.pdf")
