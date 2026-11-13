import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

n = 4
rng = np.random.default_rng(seed=2026)
ones = sorted(rng.choice(2 ** n, size=2 ** (n - 1), replace=False))
balanced = [1 if x in ones else 0 for x in range(2 ** n)]
constant = [1] * 2 ** n                  # f(x) = 1 for every x
print("balanced f is 1 on x =", [int(x) for x in ones])

def dj_circuit(table):
    qc = QuantumCircuit(n + 1, n)        # qubit n is the output y
    qc.x(n)
    qc.h(range(n + 1))
    for x, fx in enumerate(table):       # bit oracle from the table
        if fx:
            zeros = [q for q in range(n) if not (x >> q) & 1]
            if zeros:
                qc.x(zeros)
            qc.mcx(list(range(n)), n)
            if zeros:
                qc.x(zeros)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

sampler = StatevectorSampler(seed=5)
for label, table in [("constant", constant), ("balanced", balanced)]:
    qc = dj_circuit(table)
    counts = sampler.run([qc], shots=1000).result()[0].data.c
    counts = dict(sorted(counts.get_counts().items()))
    print(f"{label}: P(0000) = {counts.get('0000', 0) / 1000:.3f}",
          f" counts = {counts}")
