# Matrices acting on vectors, and why the order of products matters
import numpy as np

X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])
v = np.array([0.6, 0.8])

print("X v =", X @ v, "  Z v =", Z @ v)
print("X Z =\n", X @ Z)
print("Z X =\n", Z @ X)
print("XZ equals ZX? ", np.array_equal(X @ Z, Z @ X))
print("XZ equals -ZX?", np.array_equal(X @ Z, -(Z @ X)))

# (X Z) v means: apply Z first, then X
print("(X Z) v =", (X @ Z) @ v, " X (Z v) =", X @ (Z @ v))

