import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.quantum_info import Statevector

n, N, j = 3, 8, 6                         # transform |6> = |110>
qc = QuantumCircuit(n)
qc.x([1, 2])                              # q2 q1 q0 = 1 1 0
qc.append(QFTGate(n), range(n))
amps = Statevector(qc).data

print(" k  |amp|   phase (turns)   expected j*k/N mod 1")
for k in range(N):
    turns = (np.angle(amps[k]) / (2 * np.pi)) % 1
    print(f" {k}  {abs(amps[k]):.3f}   {turns:.3f}"
          f"           {(j * k / N) % 1:.3f}")

# Product formula: qubit l carries phase j / 2**(n - l) turns
factors = []
for l in range(n):
    t = (j / 2 ** (n - l)) % 1
    print(f"qubit {l}: (|0> + e^(2 pi i * {t:.3f}) |1>) / sqrt2")
    factors.append(np.array([1, np.exp(2j * np.pi * t)])
                   / np.sqrt(2))
product = np.kron(np.kron(factors[2], factors[1]), factors[0])
print("product state matches:", np.allclose(product, amps))
