# Born rule: outcome probabilities in the Z, X and Y bases
import numpy as np
from qiskit.quantum_info import Statevector, Operator

s = 1 / np.sqrt(2)
bases = {                               # two unit vectors each
    "Z": (np.array([1, 0]), np.array([0, 1])),
    "X": (np.array([s, s]), np.array([s, -s])),
    "Y": (np.array([s, 1j * s]), np.array([s, -1j * s])),
}
for amps in ([0.6, 0.8], [0.6, 0.8j]):
    psi = Statevector(amps)
    print("state", amps)
    for name, (b0, b1) in bases.items():
        p0 = abs(np.vdot(b0, psi.data)) ** 2      # |<b0|psi>|^2
        p1 = abs(np.vdot(b1, psi.data)) ** 2
        print(f"  {name} basis: P(first) = {p0:.4f},"
              f" P(second) = {p1:.4f}")

# Same X-basis numbers: rotate with H, then read Z probabilities
H = Operator(np.array([[1, 1], [1, -1]]) * s)
print("via H, then Z  :",
      np.round(Statevector([0.6, 0.8]).evolve(H).probabilities(), 4))
