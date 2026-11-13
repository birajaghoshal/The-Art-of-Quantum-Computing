# Grover search for the satisfying assignments (M = 2 of N = 16)
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
from groverlib import diffuser, best_k
from satlib import sat_oracle, CLAUSES

var = QuantumRegister(4, "x")
cl = QuantumRegister(len(CLAUSES), "cl")
out, c = QuantumRegister(1, "out"), ClassicalRegister(4, "c")
qc = QuantumCircuit(var, cl, out, c)
qc.h(var)
qc.x(out)
qc.h(out)                                  # |-> for phase kickback
k = best_k(16, 2)
for _ in range(k):
    qc.compose(sat_oracle(), [*var, *cl, *out], inplace=True)
    qc.compose(diffuser(4), var, inplace=True)
qc.measure(var, c)

sampler = StatevectorSampler(seed=8)
counts = sampler.run([qc], shots=1000).result()[0].data.c \
    .get_counts()
top = sorted(counts.items(), key=lambda kv: -kv[1])[:4]
print("iterations:", k)
print("most frequent assignments:", dict(top))
