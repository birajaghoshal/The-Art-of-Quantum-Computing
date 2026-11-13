# The three Pauli matrices and their algebra, checked with Operator.
import numpy as np
from qiskit.circuit.library import XGate, YGate, ZGate
from qiskit.quantum_info import Operator

X, Y, Z = Operator(XGate()), Operator(YGate()), Operator(ZGate())
I = Operator(np.eye(2))

# A @ B means "first B, then A", exactly like matrix products.
print("X^2 = I:", X @ X == I, " Y^2 = I:", Y @ Y == I,
      " Z^2 = I:", Z @ Z == I)
print("XY = iZ: ", X @ Y == 1j * Z)
print("XY = -YX:", X @ Y == -(Y @ X))
print("XYZ = iI:", X @ Y @ Z == 1j * I)
