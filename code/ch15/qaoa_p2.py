"""Optimise QAOA at p = 1 and p = 2, then sample candidate cuts."""
import numpy as np
from scipy.optimize import minimize
from qiskit.primitives import (StatevectorEstimator,
                               StatevectorSampler)
from maxcut_qaoa import EDGES, N, cost_hamiltonian, qaoa_circuit

H, est = cost_hamiltonian(), StatevectorEstimator()
cut = lambda s: sum(s[N - 1 - i] != s[N - 1 - j] for i, j in EDGES)
rng = np.random.default_rng(3)
# exact cut-size distribution (0 to 6) of a uniform random guess
random_guess = np.array([2, 0, 2, 12, 10, 4, 2]) / 32
hists = {}                         # p -> sampled cut distribution
for p in (1, 2):
    qc = qaoa_circuit(p)           # parameter order: b[...], g[...]
    f = lambda x: float(est.run([(qc, H, x)]).result()[0].data.evs)
    best = None
    for start in range(5):         # a few random starting points
        x0 = rng.uniform(0, np.pi / 2, size=2 * p)
        r = minimize(f, x0, method="COBYLA",
                     options={"maxiter": 200})
        best = r if best is None or r.fun < best.fun else best
    print(f"p = {p}: expected cut = {-best.fun:.4f}, "
          f"ratio = {-best.fun / 6:.4f}")
    print("  (b[0..p-1], g[0..p-1]) =", np.round(best.x, 3))
    # Sample the optimised circuit to obtain actual cuts
    qm = qc.assign_parameters(best.x)
    qm.measure_all()
    counts = StatevectorSampler(seed=42).run([qm], shots=2000) \
        .result()[0].data.meas.get_counts()
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:2]
    print("  most frequent bitstrings (q4...q0):")
    for s, c in top:
        print(f"    {s}: {c:4d} shots, cut = {cut(s)}")
    hits = sum(c for s, c in counts.items() if cut(s) == 6)
    print(f"  shots giving the maximum cut: {hits / 2000:.3f}")
    hists[p] = np.zeros(7)
    for s, c in counts.items():
        hists[p][cut(s)] += c / 2000

# Plotting code for Figure 15.8: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.bar(np.arange(7) - 0.27, random_guess, 0.27, color="#5B6B7F",
       label="random guess")
for p, col, dx in [(1, "#1F5FBF", 0.0), (2, "#0F9D8C", 0.27)]:
    ax.bar(np.arange(7) + dx, hists[p], 0.27, color=col,
           label=f"p = {p}")
ax.set_xlabel("cut size")
ax.set_ylabel("probability")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch15/qaoa_cuts.pdf")
