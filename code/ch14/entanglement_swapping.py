# Entanglement swapping: entangle q0 and q3, which never interact.
from qiskit import QuantumCircuit
from qiskit.quantum_info import (Statevector, partial_trace,
                                 state_fidelity)

qc = QuantumCircuit(4)
qc.h(0); qc.cx(0, 1)            # pair A: q0 (Alice) - q1 (relay)
qc.h(2); qc.cx(2, 3)            # pair B: q2 (relay) - q3 (Bob)
before = partial_trace(Statevector(qc), [1, 2])
qc.cx(1, 2); qc.h(1)            # Bell measurement at the relay...
qc.cx(2, 3); qc.cz(1, 3)        # ...with deferred corrections on q3
after = partial_trace(Statevector(qc), [1, 2])

bell = QuantumCircuit(2)
bell.h(0); bell.cx(0, 1)
target = Statevector(bell)
print(f"Fidelity of (q0, q3) with a Bell pair, before: "
      f"{state_fidelity(before, target):.3f}")
print(f"Fidelity of (q0, q3) with a Bell pair, after : "
      f"{state_fidelity(after, target):.3f}")
