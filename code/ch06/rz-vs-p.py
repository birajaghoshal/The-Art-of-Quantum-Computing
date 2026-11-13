# RZ(lam) and P(lam) differ only by the global phase exp(-i lam / 2).
import numpy as np
from qiskit.circuit.library import RZGate, PhaseGate
from qiskit.quantum_info import Operator, Statevector

lam = 1.2
RZ, P = Operator(RZGate(lam)), Operator(PhaseGate(lam))
print("RZ diagonal:", np.round(np.diag(RZ.data), 4).tolist())
print("P  diagonal:", np.round(np.diag(P.data), 4).tolist())
print("RZ == P:                  ", RZ == P)
print("RZ == exp(-i lam/2) * P:  ", RZ == np.exp(-0.5j * lam) * P)
print("RZ equiv P:               ", RZ.equiv(P))

plus = Statevector.from_label("+")
a, b = plus.evolve(RZ), plus.evolve(P)
print("states equal:", a == b, "  states equiv:", a.equiv(b))
