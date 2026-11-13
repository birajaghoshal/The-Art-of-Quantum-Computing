from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, TGate
from qiskit.primitives import StatevectorSampler

t = 3                                     # counting qubits q0 to q2
qc = QuantumCircuit(t + 1, t)             # q3 holds the eigenstate
qc.x(t)                                   # |1> is an eigenstate of T
qc.h(range(t))
ct = TGate().control(1)                   # controlled-T
for k in range(t):
    for _ in range(2 ** k):               # controlled-T^(2^k)
        qc.append(ct, [k, t])
qc.append(QFTGate(t).inverse(), range(t))
qc.measure(range(t), range(t))

sampler = StatevectorSampler(seed=21)
result = sampler.run([qc], shots=1000).result()
counts = result[0].data.c.get_counts()
print("counts:", counts)
best = max(counts, key=counts.get)
print(f"estimate: theta = {int(best, 2)}/{2 ** t}"
      f" = {int(best, 2) / 2 ** t}")
print("gate counts:", dict(qc.count_ops()))
