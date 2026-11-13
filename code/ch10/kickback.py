import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

table = [0, 0, 1, 0, 1, 1, 0, 1]        # same f as before
n = 3

qc = QuantumCircuit(n + 1)
qc.x(n)
qc.h(range(n + 1))                      # inputs: |+>; output: |->
for x, fx in enumerate(table):          # bit oracle from the table
    if fx:
        zeros = [q for q in range(n) if not (x >> q) & 1]
        if zeros:
            qc.x(zeros)
        qc.mcx(list(range(n)), n)
        if zeros:
            qc.x(zeros)

amps = Statevector(qc).data
# Output qubit is |-> = (|0> - |1>)/sqrt2, so the amplitude of
# |0>|x> times sqrt(2) times sqrt(8) is the sign attached to |x>.
for x in range(8):
    sign = np.real(amps[x]) * np.sqrt(2) * np.sqrt(8)
    print(f"x = {x:03b}  f(x) = {table[x]}  sign = {sign:+.0f}")
