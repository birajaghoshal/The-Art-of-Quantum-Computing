# Deferred measurement: controlled gates replace feed-forward.
# Compare Bob's Bloch vector with the input for several states.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import (Statevector, DensityMatrix,
                                 partial_trace, Pauli,
                                 state_fidelity)

def bloch(rho):
    return np.array([rho.expectation_value(Pauli(p)).real
                     for p in "XYZ"])

def fmt(v):
    return " ".join(f"{x + 0.0:+.3f}" for x in np.round(v, 3))

print("theta   phi  input (x, y, z)       Bob (x, y, z)         F")
for theta, phi in [(0.0, 0.0), (np.pi / 2, 0.0), (1.1, 0.7),
                   (2.5, -2.0)]:
    prep = QuantumCircuit(1)
    prep.ry(theta, 0); prep.rz(phi, 0)
    qc = QuantumCircuit(3)
    qc.compose(prep, [0], inplace=True)
    qc.h(1); qc.cx(1, 2)
    qc.cx(0, 1); qc.h(0)
    qc.cx(1, 2); qc.cz(0, 2)          # corrections, now quantum
    bob = partial_trace(Statevector(qc), [0, 1])
    target = DensityMatrix(prep)
    print(f"{theta:5.2f} {phi:+5.2f}  {fmt(bloch(target))}  "
          f"{fmt(bloch(bob))}  {state_fidelity(bob, target):.4f}")
