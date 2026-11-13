"""Build a two-qubit Hamiltonian and evaluate it three ways."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.primitives import StatevectorEstimator

# Label "ZI" means Z on qubit 1 and I on qubit 0 (little-endian)
H = SparsePauliOp.from_list([("ZI", 0.5), ("IZ", -1.0),
                             ("XX", 0.25)])
print(H)
print("Eigenvalues:", np.round(np.linalg.eigvalsh(H.to_matrix()), 4))

# Prepare |q1 q0> = |01>, i.e. flip qubit 0 only
qc = QuantumCircuit(2)
qc.x(0)
ev_sv = Statevector(qc).expectation_value(H).real
ev_est = StatevectorEstimator().run([(qc, H)]).result()[0].data.evs
print(f"<01|H|01> via Statevector: {ev_sv:.4f}")
print(f"<01|H|01> via Estimator  : {float(ev_est):.4f}")

# Terms that can share one measurement setting
for group in H.group_commuting(qubit_wise=True):
    print("measure together:", group.paulis.to_labels())
