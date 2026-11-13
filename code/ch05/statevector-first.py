# Exact amplitudes and probabilities of the three-coin circuit.
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(3)       # no measurements: Statevector needs a
qc.h(0)                      # purely unitary circuit
qc.x(1)
qc.ry(2 * pi / 3, 2)

psi = Statevector.from_instruction(qc)
print("dimension:", psi.dim)
for label, amp in psi.to_dict().items():
    print(f"  |{label}>  amplitude {amp.real:+.4f}")

probs = psi.probabilities_dict()
print("probabilities:")
for label, p in sorted(probs.items()):
    print(f"  {label}: {p:.4f}")
print("P(qubit 2 = 1):", round(psi.probabilities([2])[1], 4))
