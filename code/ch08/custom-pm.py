# A hand-built PassManager that tidies up a wasteful circuit
from qiskit import QuantumCircuit
from qiskit.circuit.library import CXGate, HGate
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import (
    RemoveBarriers, InverseCancellation, CommutativeCancellation,
    Optimize1qGatesDecomposition, RemoveDiagonalGatesBeforeMeasure)

qc = QuantumCircuit(3)
qc.h(0); qc.h(0)                   # H H = I
qc.cx(0, 1); qc.cx(0, 1)           # CX CX = I
qc.barrier()
qc.rz(0.3, 2); qc.rz(-0.1, 2); qc.h(2)   # rotations to merge
qc.cx(1, 2); qc.rz(0.5, 1); qc.cx(1, 2)  # RZ on control commutes
qc.sx(1)
qc.z(2)                            # diagonal, just before measuring
qc.measure_all()

pm = PassManager([
    RemoveBarriers(),
    InverseCancellation([CXGate(), HGate()]),
    CommutativeCancellation(),
    Optimize1qGatesDecomposition(basis=["rz", "sx", "x"]),
    RemoveDiagonalGatesBeforeMeasure(),
])
out = pm.run(qc)
print("Before:", dict(qc.count_ops()))
print("After: ", dict(out.count_ops()))
print("Depth before/after:", qc.depth(), "/", out.depth())
print(out.draw("text", fold=68))
