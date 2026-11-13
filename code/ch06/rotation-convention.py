# RX, RY, RZ are exp(-i theta P / 2): note the factor of one half.
import numpy as np
from scipy.linalg import expm
from qiskit.circuit.library import RXGate, RYGate, RZGate
from qiskit.quantum_info import Operator, Pauli

theta = 0.9
for gate, p in [(RXGate, "X"), (RYGate, "Y"), (RZGate, "Z")]:
    by_formula = expm(-1j * theta / 2 * Pauli(p).to_matrix())
    same = np.allclose(Operator(gate(theta)).data, by_formula)
    print(f"R{p}({theta}) == exp(-i {theta} {p} / 2):", same)

X = Operator(Pauli("X"))
I = Operator(Pauli("I"))
rx = lambda t: Operator(RXGate(t))
print("RX(pi) == X:       ", rx(np.pi) == X)
print("RX(pi) == -i X:    ", rx(np.pi) == -1j * X)
print("RX(pi) equiv X:    ", rx(np.pi).equiv(X))
print("RX(2 pi) == -I:    ", rx(2 * np.pi) == -1 * I)
print("RX(4 pi) == I:     ", rx(4 * np.pi) == I)
