import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def bit_oracle(table):
    """U_f|x>|y> = |x>|y XOR f(x)>, built from a truth table."""
    n = int(np.log2(len(table)))
    qc = QuantumCircuit(n + 1)          # qubit n is the output y
    for x, fx in enumerate(table):
        if fx == 0:
            continue
        zeros = [q for q in range(n) if not (x >> q) & 1]
        if zeros:
            qc.x(zeros)                 # map |x> to |11...1>
        qc.mcx(list(range(n)), n)       # flip y when all are 1
        if zeros:
            qc.x(zeros)                 # undo the mapping
    return qc

table = [0, 0, 1, 0, 1, 1, 0, 1]        # f(x) for x = 0..7
oracle = bit_oracle(table)

# The matrix we expect: basis state index x + 8*y goes to
# x + 8*(y XOR f(x)), a permutation of the 16 basis states.
expected = np.zeros((16, 16))
for x in range(8):
    for y in range(2):
        expected[x + 8 * (y ^ table[x]), x + 8 * y] = 1

print("matches permutation:", Operator(oracle).equiv(expected))
print("gate counts:", dict(oracle.count_ops()))
