# CHSH value of a Bell pair with the ideal StatevectorEstimator
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

def bob(angle):                  # Bob measures along an angle in ZX
    return SparsePauliOp.from_sparse_list(
        [("Z", [1], np.cos(angle)), ("X", [1], np.sin(angle))], 2)

alice = [SparsePauliOp.from_sparse_list([(p, [0], 1)], 2)
         for p in "ZX"]          # Alice measures Z or X on q0
theta = np.pi / 4
bobs = [bob(theta), bob(-theta)]
terms = [alice[x].compose(bobs[y]) for x in (0, 1) for y in (0, 1)]

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)                      # |Phi+>

E = StatevectorEstimator().run([(qc, terms)]).result()[0].data.evs
for (x, y), e in zip([(0, 0), (0, 1), (1, 0), (1, 1)], E):
    print(f"E(x={x}, y={y}) = {e:+.4f}")
S = E[0] + E[1] + E[2] - E[3]
print(f"S = {S:.4f}   (2*sqrt(2) = {2 * np.sqrt(2):.4f})")
print(f"win probability = {0.5 + S / 8:.4f}")
