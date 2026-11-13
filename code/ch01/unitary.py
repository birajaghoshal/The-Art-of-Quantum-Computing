# Testing matrices for the Hermitian and unitary properties
import numpy as np

def is_unitary(U, tol=1e-10):
    U = np.asarray(U, dtype=complex)
    n = U.shape[0]
    return (U.shape == (n, n)
            and np.allclose(U.conj().T @ U, np.eye(n), atol=tol))

def is_hermitian(M, tol=1e-10):
    M = np.asarray(M, dtype=complex)
    return np.allclose(M, M.conj().T, atol=tol)

Y = np.array([[0, -1j], [1j, 0]])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
S = np.array([[1, 0], [0, 1j]])
M = np.array([[1, 1], [0, 1]])
for name, A in [("Y", Y), ("H", H), ("S", S), ("M", M)]:
    print(f"{name}: unitary = {is_unitary(A)!s:5}"
          f"  Hermitian = {is_hermitian(A)}")

# A unitary keeps the length of every vector; M does not
psi = np.array([0.6, 0.8j])
print(f"|psi| = {np.linalg.norm(psi):.4f},"
      f" |S psi| = {np.linalg.norm(S @ psi):.4f},"
      f" |M psi| = {np.linalg.norm(M @ psi):.4f}")
