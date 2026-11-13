# Eigenvalues, eigenvectors and the spectral decomposition
import numpy as np
np.set_printoptions(precision=4, suppress=True)

A = np.array([[2.0, 1.0], [1.0, 2.0]])        # real symmetric
vals, vecs = np.linalg.eigh(A)                # for Hermitian input
print("eigenvalues :", vals)
print("eigenvectors (columns):\n", vecs)
for k in range(2):
    ok = np.allclose(A @ vecs[:, k], vals[k] * vecs[:, k])
    print(f"A v{k} = {vals[k]:.0f} v{k}?", ok)

# Spectral decomposition: A = sum_k lambda_k v_k v_k^dagger
rebuilt = sum(vals[k] * np.outer(vecs[:, k], vecs[:, k].conj())
              for k in range(2))
print("rebuilt from eigen-pieces:\n", rebuilt)

# A unitary (here a rotation) has eigenvalues on the unit circle
t = 0.7
R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
lam = np.linalg.eigvals(R)                    # general solver
print("eigenvalues of R(0.7):", np.round(lam, 4))
print("their moduli         :", np.round(np.abs(lam), 4))
print("their angles         :", np.round(np.angle(lam), 4))
