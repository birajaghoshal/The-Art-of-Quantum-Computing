# Classical feed-forward with if_test: steer a Bell partner to |0>
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

q = QuantumRegister(2, "q")
c = ClassicalRegister(2, "c")
qc = QuantumCircuit(q, c)
qc.h(0)
qc.cx(0, 1)                       # Bell pair: outcomes 00 or 11
qc.measure(0, c[0])               # read q0 halfway through
with qc.if_test((c[0], 1)):       # only if q0 gave 1 ...
    qc.x(1)                       # ... flip q1 back to 0
qc.measure(1, c[1])
print(qc.draw("text", fold=68))

sampler = AerSampler.from_backend(AerSimulator(seed_simulator=42))
counts = (sampler.run([qc], shots=1000).result()[0]
          .data.c.get_counts())
print("Counts (c1 c0):", dict(sorted(counts.items())))
