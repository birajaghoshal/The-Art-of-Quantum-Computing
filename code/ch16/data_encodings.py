"""Three ways to load numbers into qubits."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from qiskit.quantum_info import Statevector

# 1) Basis encoding: the integer 6 = 110 in binary on three qubits
qc = QuantumCircuit(3)
qc.x([1, 2])                       # q2 q1 q0 = 1 1 0
print("basis    :", {str(k): float(v) for k, v in
                     Statevector(qc).probabilities_dict().items()})

# 2) Angle encoding: one feature per qubit, x -> RY(x)
x = np.array([0.4, 1.9])
qc = QuantumCircuit(2)
for i, xi in enumerate(x):
    qc.ry(xi, i)
probs = Statevector(qc).probabilities_dict()
print("angle    :", {str(k): round(float(v), 4)
                     for k, v in probs.items()})
print("  check P(00) = cos^2(0.2) cos^2(0.95):",
      round(np.cos(0.2) ** 2 * np.cos(0.95) ** 2, 4))

# 3) Amplitude encoding: four numbers in the amplitudes of 2 qubits
v = np.array([3.0, 1.0, 2.0, 1.0])
amp = v / np.linalg.norm(v)
qc = QuantumCircuit(2)
qc.append(StatePreparation(amp), [0, 1])
print("amplitude:", np.round(Statevector(qc).data.real, 4))
print("  target :", np.round(amp, 4))
cost = qc.decompose(reps=6).count_ops()
print("  gates after decomposition:", dict(cost))
