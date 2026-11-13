# Expectation values of Z, X and Y: exact, and estimated from shots
import numpy as np
from qiskit.quantum_info import Statevector, Operator, Pauli

psi = Statevector([0.6, 0.8j])
for p in "ZXY":
    ev = psi.expectation_value(Pauli(p)).real
    print(f"<{p}> exact            = {ev:+.4f}")

shots = 4000
psi.seed(113)
c = psi.sample_counts(shots)
z_est = (c.get("0", 0) - c.get("1", 0)) / shots  # 0 -> +1, 1 -> -1
print(f"<Z> from {shots} shots = {z_est:+.4f}"
      f"  (SE {np.sqrt((1 - z_est**2) / shots):.4f})")

# For <Y>, first rotate the Y basis onto the Z basis, then count
U = Operator(np.array([[1, -1j], [1, 1j]]) / np.sqrt(2))
rotated = psi.evolve(U)
rotated.seed(114)
c = rotated.sample_counts(shots)
y_est = (c.get("0", 0) - c.get("1", 0)) / shots
print(f"<Y> from {shots} shots = {y_est:+.4f}"
      f"  (SE {np.sqrt((1 - y_est**2) / shots):.4f})")
