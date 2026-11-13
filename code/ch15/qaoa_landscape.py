"""p = 1 QAOA landscape: expected cut on a grid of (gamma, beta)."""
import numpy as np
from qiskit.primitives import StatevectorEstimator
from maxcut_qaoa import cost_hamiltonian, qaoa_circuit

H = cost_hamiltonian()
qc = qaoa_circuit(1)               # parameters sorted: b[0], g[0]
gammas = np.linspace(0, np.pi, 61)
betas = np.linspace(0, np.pi / 2, 31)
G, B = np.meshgrid(gammas, betas)
grid = np.stack([B, G], axis=-1)   # shape (31, 61, 2)

# One estimator call evaluates all 1891 parameter pairs
res = StatevectorEstimator().run([(qc, H, grid)]).result()[0]
evs = res.data.evs
cut = -evs                         # expected cut size
i, j = np.unravel_index(np.argmax(cut), cut.shape)
print(f"best grid point: gamma = {G[i, j]:.3f}, "
      f"beta = {B[i, j]:.3f}")
print(f"expected cut there: {cut[i, j]:.4f} (max possible 6)")
print(f"expected cut at gamma = beta = 0: {cut[0, 0]:.4f}")

# Plotting code for Figure 15.7: see the companion repository.
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3.6))
im = ax.pcolormesh(G, B, cut, cmap="viridis", shading="auto",
                   rasterized=True)
ax.plot(G[i, j], B[i, j], "*", color="#F28C28", ms=12)
fig.colorbar(im, ax=ax, label="expected cut size")
ax.set_xlabel(r"$\gamma$")
ax.set_ylabel(r"$\beta$")
fig.tight_layout()
fig.savefig("figures/ch15/qaoa_landscape.pdf")
