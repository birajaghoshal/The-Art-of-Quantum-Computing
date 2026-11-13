# CZ, CY and controlled rotations, checked with Operator
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate
from qiskit.quantum_info import Operator

def two_qubit(*steps):
    qc = QuantumCircuit(2)
    for name, args in steps:
        getattr(qc, name)(*args)
    return Operator(qc)

cz01 = two_qubit(("cz", (0, 1)))
cz10 = two_qubit(("cz", (1, 0)))
print("CZ is symmetric:", cz01.equiv(cz10))
print("CZ = H CX H on target:",
      cz01.equiv(two_qubit(("h", (1,)), ("cx", (0, 1)),
                           ("h", (1,)))))
print("CY = Sdg CX S on target:", two_qubit(("cy", (0, 1))).equiv(
      two_qubit(("sdg", (1,)), ("cx", (0, 1)), ("s", (1,)))))

# A controlled version of any gate via .control()
cry = RYGate(np.pi / 3).control(1)
qc = QuantumCircuit(2)
qc.append(cry, [0, 1])           # control q0, target q1
print("CRY(pi/3) matrix (real part):")
print(np.real(Operator(qc).data).round(3))
