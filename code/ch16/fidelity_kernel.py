"""Fidelity quantum kernel k(x, x') = |<phi(x)|phi(x')>|^2."""
import numpy as np
from qiskit.quantum_info import Statevector

def feature_states(fmap, X):
    # One statevector per data point, stacked as rows
    return np.array([Statevector(fmap.assign_parameters(x)).data
                     for x in X])

def kernel(SA, SB):
    # All overlaps at once: entry (i, j) = |<a_i|b_j>|^2
    return np.abs(SA.conj() @ SB.T) ** 2

if __name__ == "__main__":
    from qiskit.circuit.library import zz_feature_map
    from moons_data import load
    Xtr, Xte, ytr, yte = load(top=np.pi / 2)
    order = np.argsort(ytr)                # class 0 first, then 1
    S = feature_states(zz_feature_map(2, reps=2), Xtr[order])
    K = kernel(S, S)
    print("kernel shape:", K.shape)
    print("diagonal all 1:", np.allclose(np.diag(K), 1))
    print("symmetric:", np.allclose(K, K.T))
    print("rank:", np.linalg.matrix_rank(K, tol=1e-8))
    # Plotting code for Figure 16.3: see the companion repository.
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    im = ax.imshow(K, cmap="viridis", vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label="kernel value")
    ax.set_xlabel("training point (sorted by class)")
    ax.set_ylabel("training point")
    fig.tight_layout()
    fig.savefig("figures/ch16/kernel_matrix.pdf")
