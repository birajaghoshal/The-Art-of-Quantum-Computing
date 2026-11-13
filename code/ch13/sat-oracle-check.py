# Test the clause-built oracle on all 16 assignments
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from satlib import sat_oracle, satisfied

oracle = sat_oracle()
signs = []
for x in range(16):
    prep = QuantumCircuit(oracle.num_qubits)
    for i in range(4):
        if (x >> i) & 1:
            prep.x(i)
    prep.x(-1)
    prep.h(-1)                         # out (last) qubit in |->
    before = Statevector(prep)
    after = before.evolve(oracle)
    signs.append(int(np.round(np.real(before.inner(after)))))
print("phase per assignment x = 0..15:", signs)
ok = all((s == -1) == satisfied(x) for x, s in enumerate(signs))
print("oracle flips exactly the solutions:", ok)
print("oracle size:", oracle.num_qubits, "qubits,",
      dict(oracle.count_ops()))
