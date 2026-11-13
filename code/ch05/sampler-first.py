# Sample the three-coin circuit with the ideal StatevectorSampler.
from math import pi
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.h(0)
qc.x(1)
qc.ry(2 * pi / 3, 2)
qc.measure_all()

sampler = StatevectorSampler(seed=2026)
job = sampler.run([qc], shots=1000)     # a list of PUBs
result = job.result()                   # a PrimitiveResult
counts = result[0].data.meas.get_counts()
print("counts:", dict(sorted(counts.items())))

shots = sum(counts.values())
for label, n in sorted(counts.items()):
    print(f"  {label}: {n:4d}  frequency {n / shots:.3f}")
