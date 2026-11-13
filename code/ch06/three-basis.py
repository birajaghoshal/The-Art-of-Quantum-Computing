# Recover a Bloch vector from counts in the Z, X and Y bases.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector, SparsePauliOp

prep = QuantumCircuit(1)          # the state we pretend not to know
prep.ry(1.1, 0)
prep.rz(0.6, 0)

def in_basis(basis):
    qc = prep.copy()
    if basis == "X":
        qc.h(0)                   # X basis -> Z basis
    elif basis == "Y":
        qc.sdg(0)                 # Y basis -> X basis ...
        qc.h(0)                   # ... -> Z basis
    qc.measure_all()
    return qc

shots = 4000
pubs = [in_basis(b) for b in "XYZ"]
rng = np.random.default_rng(99)       # fresh draws for each PUB
res = StatevectorSampler(seed=rng).run(pubs, shots=shots).result()
exact = Statevector(prep)
for b, r in zip("XYZ", res):
    c = r.data.meas.get_counts()
    est = (c.get("0", 0) - c.get("1", 0)) / shots
    ev = exact.expectation_value(SparsePauliOp(b)).real
    print(f"<{b}> from counts {est:+.3f}   exact {ev:+.3f}")
