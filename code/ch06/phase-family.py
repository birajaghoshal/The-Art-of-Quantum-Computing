# S, T, their inverses and the general phase gate P(lambda).
import numpy as np
from fractions import Fraction
from qiskit.circuit.library import (PhaseGate, SGate, SdgGate,
                                    TGate, TdgGate, ZGate)
from qiskit.quantum_info import Operator

S, Sdg = Operator(SGate()), Operator(SdgGate())
T, Tdg = Operator(TGate()), Operator(TdgGate())
Z, I = Operator(ZGate()), Operator.from_label("I")

for name, op in [("S", S), ("Sdg", Sdg), ("T", T), ("Tdg", Tdg)]:
    turn = np.angle(op.data[1, 1]) / np.pi     # phase in units of pi
    frac = Fraction(turn).limit_denominator(8)
    print(f"{name:3s} = diag(1, exp(i*({frac})*pi))")

print("S = P(pi/2):", S == Operator(PhaseGate(np.pi / 2)))
print("T = P(pi/4):", T == Operator(PhaseGate(np.pi / 4)))
print("T T = S:    ", T @ T == S)
print("S S = Z:    ", S @ S == Z)
print("S Sdg = I:  ", S @ Sdg == I)
print("T^8 = I:    ", T.power(8) == I)
