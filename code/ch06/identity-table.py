# A table of single-qubit identities, checked two ways.
import numpy as np
from qiskit.quantum_info import Operator
from qiskit.circuit.library import (HGate, XGate, YGate, ZGate,
                                    SGate, SdgGate, TGate, SXGate,
                                    RXGate, RZGate)

H, X, Y, Z = [Operator(g()) for g in (HGate, XGate, YGate, ZGate)]
S, Sdg, T, SX = [Operator(g()) for g in (SGate, SdgGate, TGate,
                                         SXGate)]
a = 0.37                                  # any angle will do
rows = [                                  # (text, left, right)
    ("H X H = Z", H @ X @ H, Z),
    ("H Y H = Y", H @ Y @ H, Y),
    ("S X Sdg = Y", S @ X @ Sdg, Y),
    ("T T = S", T @ T, S),
    ("SX SX = X", SX @ SX, X),
    ("SX = RX(pi/2)", SX, Operator(RXGate(np.pi / 2))),
    ("H RZ(a) H = RX(a)", H @ Operator(RZGate(a)) @ H,
     Operator(RXGate(a))),
    ("X Z = Z X", X @ Z, Z @ X),
]
print(f"{'identity':20s} {'equiv':>6s} {'exact':>6s}")
for text, left, right in rows:
    print(f"{text:20s} {str(left.equiv(right)):>6s}"
          f" {str(left == right):>6s}")
