"""Pauli twirling turns a coherent CX error into Pauli noise."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RZZGate
from qiskit.quantum_info import Operator, Pauli, Statevector

eps, rng = 0.1, np.random.default_rng(3)
cx = QuantumCircuit(2)
cx.cx(0, 1)
CX = Operator(cx).data
noisy_cx = Operator(RZZGate(eps)).data @ CX    # CX, then a ZZ error
paulis = [Pauli(a + b) for a in "IXYZ" for b in "IXYZ"]
P = [p.to_matrix() for p in paulis]
# Partner Q = CX P CX, chosen so that Q . CX . P = CX exactly
Q = [p.evolve(cx, frame="s").to_matrix() for p in paulis]

prep = QuantumCircuit(2)
prep.ry(0.7, 0)
prep.ry(1.9, 1)
psi0 = Statevector(prep).data

def infidelity(n_gates, twirl, samples=1):
    ideal = np.linalg.matrix_power(CX, n_gates) @ psi0
    fids = []
    for _ in range(samples):
        psi = psi0
        for k in rng.integers(16, size=n_gates) * twirl:
            psi = Q[k] @ (noisy_cx @ (P[k] @ psi))
        fids.append(abs(np.vdot(ideal, psi)) ** 2)
    return 1 - np.mean(fids)

ns = np.arange(0, 41, 2)
bare = [infidelity(n, 0) for n in ns]
twirled = [infidelity(n, 1, samples=400) for n in ns]
for n in [2, 10, 20, 30, 40]:
    i = list(ns).index(n)
    print(f"{n:2d} CX gates: coherent 1-F = {bare[i]:.4f}   "
          f"twirled 1-F = {twirled[i]:.4f}")
