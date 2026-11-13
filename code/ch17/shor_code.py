"""Shor's nine-qubit code survives any single-qubit Pauli error."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import (Statevector, partial_trace,
                                 state_fidelity)

def prepare(qc):
    qc.ry(2.1, 0)
    qc.rz(-0.4, 0)                     # an arbitrary input state psi

def round_trip(errors=()):
    qc = QuantumCircuit(9)
    prepare(qc)
    qc.cx([0, 0], [3, 6])              # outer layer: phase-flip code
    qc.h([0, 3, 6])
    for b in (0, 3, 6):                # inner layer: bit-flip code
        qc.cx([b, b], [b + 1, b + 2])
    for pauli, q in errors:
        getattr(qc, pauli.lower())(q)  # e.g. ("Y", 4) -> qc.y(4)
    for b in (0, 3, 6):                # undo inner layer + vote
        qc.cx([b, b], [b + 1, b + 2])
        qc.ccx(b + 2, b + 1, b)
    qc.h([0, 3, 6])                    # undo outer layer + vote
    qc.cx([0, 0], [3, 6])
    qc.ccx(6, 3, 0)
    rho = partial_trace(Statevector(qc), list(range(1, 9)))
    return state_fidelity(rho, target)

psi = QuantumCircuit(1)
prepare(psi)
target = Statevector(psi)
print(f"no error           : fidelity {round_trip():.4f}")
for p in "XYZ":
    worst = min(round_trip([(p, q)]) for q in range(9))
    print(f"{p} on any qubit     : worst fidelity {worst:.4f}")
for pair in [[("X", 0), ("X", 3)], [("X", 0), ("X", 1)],
             [("Z", 0), ("Z", 3)]]:
    label = " + ".join(f"{p}{q}" for p, q in pair)
    print(f"two errors {label:8s}: fidelity {round_trip(pair):.4f}")
