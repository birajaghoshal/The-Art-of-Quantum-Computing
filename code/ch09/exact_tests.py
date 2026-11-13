# Exact tests: equality versus equivalence up to global phase.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

a = QuantumCircuit(1); a.rz(0.8, 0)
b = QuantumCircuit(1); b.p(0.8, 0)
Ua, Ub = Operator(a), Operator(b)
print("RZ == P        :", Ua == Ub)
print("RZ equiv P     :", Ua.equiv(Ub))
phase = np.angle(Ua.data[0, 0] / Ub.data[0, 0])
print(f"Global phase   : {phase:.4f} rad")

plus = Statevector.from_label("+")
minus = Statevector.from_label("-")
print("|+> equiv |->  :", plus.equiv(minus))
print("|-> equiv -|-> :", minus.equiv(-1 * minus))
