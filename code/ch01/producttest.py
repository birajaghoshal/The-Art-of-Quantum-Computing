# Can a length-4 vector be written as a (x) b? A determinant test
import numpy as np

def is_product(psi, tol=1e-10):
    """Is psi (length 4) equal to kron(a, b)? Also return det."""
    M = np.asarray(psi, dtype=complex).reshape(2, 2)
    return abs(np.linalg.det(M)) < tol, np.linalg.det(M)

s = 1 / np.sqrt(2)
candidates = {
    "kron([1,0],[s,s])": np.kron([1, 0], [s, s]),
    "[0.5,0.5,0.5,0.5]": np.array([0.5, 0.5, 0.5, 0.5]),
    "[s,0,0,s]": np.array([s, 0, 0, s]),
    "[0.6,0,0,0.8]": np.array([0.6, 0, 0, 0.8]),
    "[0.5,0.5,0.5,-0.5]": np.array([0.5, 0.5, 0.5, -0.5]),
}
for name, psi in candidates.items():
    ok, d = is_product(psi)
    print(f"{name:20s} det = {abs(d):.4f}  product? {ok}")
