# Gates are unitary operators: evolve a state, then undo it
import numpy as np
from qiskit.quantum_info import Statevector, Operator

psi = Statevector([0.6, 0.8])
H = Operator(np.array([[1, 1], [1, -1]]) / np.sqrt(2))
S = Operator(np.array([[1, 0], [0, 1j]]))
print("H unitary?", H.is_unitary(), "  S unitary?", S.is_unitary())

out = psi.evolve(H)
print("after H        :", np.round(out.data, 4))
print("  probabilities:", np.round(out.probabilities(), 4))
out2 = psi.evolve(S).evolve(H)          # S first, then H
print("after S, then H:", np.round(out2.data, 4))
print("  probabilities:", np.round(out2.probabilities(), 4))

# Undo: apply the adjoints in the reverse order
back = out2.evolve(H.adjoint()).evolve(S.adjoint())
print("undone         :", np.round(back.data, 4) + 0)
print("equal to psi?  :", back.equiv(psi))

M = Operator(np.array([[1, 1], [0, 1]]))   # not unitary
bad = psi.evolve(M)
total = np.linalg.norm(bad.data) ** 2       # sum of |amplitude|^2
print("M unitary?", M.is_unitary(),
      "  valid after M?", bad.is_valid())
print(f"sum of |amplitudes|^2 after M: {total:.4f}")
