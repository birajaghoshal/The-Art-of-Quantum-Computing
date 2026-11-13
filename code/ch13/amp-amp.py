# Amplitude amplification with a non-uniform state preparation A
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import grover_operator
from qiskit.quantum_info import Statevector

A = QuantumCircuit(3, name="A")   # any circuit can play this role
A.ry(1.2, 0)
A.ry(1.4, 1)
A.ry(1.6, 2)
good = "111"
oracle = QuantumCircuit(3)        # CCZ marks |111>
oracle.h(2)
oracle.ccx(0, 1, 2)
oracle.h(2)

p = Statevector(A).probabilities_dict()[good]
half = np.arcsin(np.sqrt(p))
print(f"P(good) from A alone: {p:.4f}  "
      f"(repeat A about {1/p:.1f} times classically)")
print("best k:", int(np.floor(np.pi / (4 * half))))
Q = grover_operator(oracle, state_preparation=A)
for k in range(5):
    qc = A.copy()
    for _ in range(k):
        qc.compose(Q, inplace=True)
    p_k = Statevector(qc).probabilities_dict().get(good, 0)
    print(f"k = {k}: P(good) = {p_k:.4f}, "
          f"formula {np.sin((2 * k + 1) * half) ** 2:.4f}")
