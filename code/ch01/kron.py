# Tensor (Kronecker) products of vectors and matrices
import numpy as np
np.set_printoptions(precision=4, suppress=True)

zero, one = np.array([1, 0]), np.array([0, 1])
print("e0 (x) e1 =", np.kron(zero, one))
print("e1 (x) e0 =", np.kron(one, zero))

a = np.array([0.6, 0.8])
b = np.array([1, 1j]) / np.sqrt(2)
print("a (x) b   =", np.kron(a, b))
print("b (x) a   =", np.kron(b, a))
print(f"norm of a (x) b = {np.linalg.norm(np.kron(a, b)):.4f}")

X = np.array([[0, 1], [1, 0]])
I = np.eye(2, dtype=int)
print("X (x) I =\n", np.kron(X, I))
# Mixed-product rule: (A (x) B)(a (x) b) = (A a) (x) (B b)
lhs = np.kron(X, I) @ np.kron(a, b)
print("rule holds?", np.allclose(lhs, np.kron(X @ a, I @ b)))

# Sizes grow as 2^n: lengths for 1, 2, 10, 20 and 30 factors
print("lengths:", ", ".join(f"{2**n}" for n in (1, 2, 10, 20, 30)))
