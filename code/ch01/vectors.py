# Complex vectors: combinations, inner products, norms
import numpy as np
np.set_printoptions(precision=4, suppress=True)

u = np.array([1, 1j]) / np.sqrt(2)
v = np.array([1, -1j]) / np.sqrt(2)
w = np.array([2, 1 + 1j])

print("2u + 3v           =", 2 * u + 3 * v)
# Inner product <u, w>: conjugate the FIRST vector, then sum
print("np.vdot(u, w)     =", np.round(np.vdot(u, w), 4))
print("np.dot(u, w)      =", np.round(np.dot(u, w), 4), "(no conj!)")
print("np.vdot(w, u)     =", np.round(np.vdot(w, u), 4))
print("np.vdot(u, v)     =", np.round(np.vdot(u, v), 4) + 0)

# Norm (length) and normalisation
print(f"norm of w         = {np.linalg.norm(w):.4f}")
w_hat = w / np.linalg.norm(w)
print("normalised w      =", w_hat)
print(f"its norm          = {np.linalg.norm(w_hat):.4f}")
