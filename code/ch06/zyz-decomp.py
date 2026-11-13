# Any single-qubit unitary = phase x RZ(phi) RY(theta) RZ(lam).
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, random_unitary
from qiskit.synthesis import OneQubitEulerDecomposer

target = random_unitary(2, seed=2026)          # a "mystery" gate
theta, phi, lam, phase = OneQubitEulerDecomposer("ZYZ") \
    .angles_and_phase(target.data)
print(f"theta={theta:.4f} phi={phi:.4f} lam={lam:.4f}"
      f" global phase={phase:.4f}")

qc = QuantumCircuit(1, global_phase=phase)
qc.rz(lam, 0)        # applied first
qc.ry(theta, 0)
qc.rz(phi, 0)        # applied last
print("exact match (with phase):", Operator(qc) == target)

qc.global_phase = 0
print("exact match (no phase):  ", Operator(qc) == target)
print("equiv (no phase):        ", Operator(qc).equiv(target))

# The same gate in IBM's native rz/sx form:
native = OneQubitEulerDecomposer("ZSX")(target.data)
print("ZSX form:", dict(native.count_ops()),
      " equiv:", Operator(native).equiv(target))
