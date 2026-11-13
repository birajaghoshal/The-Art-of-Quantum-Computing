# Several PUBs in one call, each with its own shot count.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

fair = QuantumCircuit(1)
fair.h(0)
fair.measure_all()

certain = QuantumCircuit(1)
certain.x(0)
certain.measure_all()

# A sampler PUB is (circuit, parameter_values, shots).
pubs = [(fair, None, 100), (certain, None, 40), fair]
rng = np.random.default_rng(11)     # one stream shared by all PUBs
sampler = StatevectorSampler(seed=rng)
result = sampler.run(pubs, shots=250).result()   # 250 = default

print("number of PUB results:", len(result))
for i, pub_result in enumerate(result):
    bits = pub_result.data.meas
    counts = dict(sorted(bits.get_counts().items()))
    print(f"PUB {i}: shots={bits.num_shots:3d}  counts={counts}")
