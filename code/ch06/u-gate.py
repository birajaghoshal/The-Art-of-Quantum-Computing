# The general single-qubit gate U(theta, phi, lam) and special cases.
import numpy as np
from qiskit.circuit.library import (UGate, HGate, XGate, PhaseGate,
                                    RXGate, RYGate)
from qiskit.quantum_info import Operator

def U(theta, phi, lam):
    return Operator(UGate(theta, phi, lam))

pi, t, lam = np.pi, 0.8, 0.5
checks = [
    ("U(pi/2, 0, pi)    == H", U(pi / 2, 0, pi), HGate()),
    ("U(pi, 0, pi)      == X", U(pi, 0, pi), XGate()),
    ("U(0, 0, lam)      == P(lam)", U(0, 0, lam), PhaseGate(lam)),
    ("U(t, 0, 0)        == RY(t)", U(t, 0, 0), RYGate(t)),
    ("U(t, -pi/2, pi/2) == RX(t)", U(t, -pi / 2, pi / 2), RXGate(t)),
]
for text, lhs, rhs in checks:
    print(f"{text:30s} {lhs == Operator(rhs)}")
print("U(0.8,0.3,0.5) =")
print(np.round(U(0.8, 0.3, 0.5).data, 3))
