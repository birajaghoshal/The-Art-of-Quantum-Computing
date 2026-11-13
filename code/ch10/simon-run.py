from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

s, n = "1011", 4
bits = [int(b) for b in reversed(s)]

qc = QuantumCircuit(2 * n, n)
qc.h(range(n))                           # superpose all x
for q in range(n):                       # Simon oracle (as before)
    qc.cx(q, n + q)
for q in range(n):
    if bits[q]:
        qc.cx(bits.index(1), n + q)
qc.h(range(n))
qc.measure(range(n), range(n))           # only the x register

sampler = StatevectorSampler(seed=42)
counts = sampler.run([qc], shots=400).result()[0].data.c.get_counts()
print("y      count   y.s mod 2")
for y, c in sorted(counts.items()):
    dot = sum(int(a) * int(b) for a, b in zip(y, s)) % 2
    print(f"{y}   {c:5d}   {dot}")
print("distinct outcomes:", len(counts))
