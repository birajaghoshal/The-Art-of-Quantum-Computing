# Three independent "coins" on three qubits.
from math import pi
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)       # three qubits, all start in |0>
qc.h(0)                      # qubit 0: a fair coin
qc.x(1)                      # qubit 1: always 1
qc.ry(2 * pi / 3, 2)         # qubit 2: a coin biased towards 1
qc.measure_all()             # adds a barrier and a register 'meas'

print(qc.draw("text", fold=68))
print("qubits:", qc.num_qubits, " classical bits:", qc.num_clbits)
print("depth:", qc.depth())
print("operations:", dict(qc.count_ops()))
