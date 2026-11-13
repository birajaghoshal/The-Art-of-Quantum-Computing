# Writing the same vector in two orthonormal bases
import numpy as np

plus = np.array([1, 1]) / np.sqrt(2)
minus = np.array([1, -1]) / np.sqrt(2)
psi = np.array([0.8, 0.6])

# Orthonormal check: B^dagger B should be the identity
B = np.column_stack([plus, minus])
print("B^dagger B =\n", np.round(B.conj().T @ B, 4) + 0.0)

# Coefficients are inner products with the basis vectors
c_plus = np.vdot(plus, psi)
c_minus = np.vdot(minus, psi)
print(f"c_plus = {c_plus:.4f}, c_minus = {c_minus:.4f}")

rebuilt = c_plus * plus + c_minus * minus
print("rebuilt psi =", np.round(rebuilt, 4))
print("equal to psi?", np.allclose(rebuilt, psi))
print(f"sum of squared coefficients = {c_plus**2 + c_minus**2:.4f}")
# All coefficients at once: B^dagger psi
print("B^dagger psi =", np.round(B.conj().T @ psi, 4))
