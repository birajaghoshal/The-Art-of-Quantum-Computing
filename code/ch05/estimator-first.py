# Expectation values of Pauli observables with StatevectorEstimator.
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

qc = QuantumCircuit(3)              # no measurements for Estimator
qc.h(0)
qc.x(1)
qc.ry(2 * pi / 3, 2)

# Labels are read right to left: the last letter acts on qubit 0.
observables = {
    "Z on q0": SparsePauliOp("IIZ"),
    "X on q0": SparsePauliOp("IIX"),
    "Z on q1": SparsePauliOp("IZI"),
    "Z on q2": SparsePauliOp("ZII"),
}
estimator = StatevectorEstimator()
pubs = [(qc, obs) for obs in observables.values()]
result = estimator.run(pubs).result()
for name, pub_result in zip(observables, result):
    print(f"<{name}> = {float(pub_result.data.evs):+.4f}")
