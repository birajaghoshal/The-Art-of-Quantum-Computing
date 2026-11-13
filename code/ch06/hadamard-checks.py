# The Hadamard gate: basis change, H^2 = I and two conjugations.
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, XGate, ZGate
from qiskit.quantum_info import Operator, Statevector

H, X, Z = Operator(HGate()), Operator(XGate()), Operator(ZGate())
print("H =", (H.data * 2 ** 0.5).round(3).real.tolist(), "/ sqrt(2)")

plus = Statevector.from_label("+")
minus = Statevector.from_label("-")
for label in ["0", "1"]:
    out = Statevector.from_label(label).evolve(H)
    print(f"H|{label}> = |+>: {out.equiv(plus)!s:5s}"
          f"   H|{label}> = |->: {out.equiv(minus)}")

print("H H = I:  ", H @ H == Operator.from_label("I"))
print("H Z H = X:", H @ Z @ H == X)
print("H X H = Z:", H @ X @ H == Z)

# Measuring in the X basis = apply H, then measure in Z.
qc = QuantumCircuit(1)
qc.h(0)              # prepare |+>
qc.h(0)              # rotate X basis onto Z basis
p0, p1 = Statevector(qc).probabilities()
print(f"|+> measured in X basis: P(0) = {p0:.3f}, P(1) = {p1:.3f}")
