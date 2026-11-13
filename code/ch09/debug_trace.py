# Step-by-step state trace: find the first gate that goes wrong.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

r = 1 / np.sqrt(2)
spec = [Statevector.from_label("100"),                  # after X
        Statevector([0, 0, 0, 0, r, r, 0, 0]),          # after H
        Statevector([0, 0, 0, 0, r, 0, 0, r])]          # after CX

def trace(qc):
    sv = Statevector.from_label("000")
    for step, inst in enumerate(qc.data):
        qubits = [qc.find_bit(q).index for q in inst.qubits]
        sv = sv.evolve(inst.operation, qubits)
        ok = sv.equiv(spec[step])
        probs = " ".join(f"{k}:{v:.2f}" for k, v in
                         sv.probabilities_dict().items() if v > 1e-9)
        verdict = "ok" if ok else "DIFFERS"
        print(f"  step {step + 1} {inst.operation.name:<2} "
              f"{str(qubits):<7}{probs:<20}{verdict}")
        if not ok:
            return

for name, xq, (c, t) in [("buggy", 0, (1, 0)), ("fix 1", 2, (1, 0)),
                         ("fix 2", 2, (0, 1))]:
    qc = QuantumCircuit(3)
    qc.x(xq); qc.h(0); qc.cx(c, t)
    print(name); trace(qc)
