# How many shots? Theory versus repeated simulated experiments.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

for E in (0.05, 0.02, 0.01):              # wanted 95% half-width
    n = np.ceil(1.96**2 * 0.25 / E**2)
    print(f"E={E:.2f}: about {n:.0f} shots")
qc = QuantumCircuit(1); qc.h(0); qc.measure_all()
sampler = StatevectorSampler(seed=np.random.default_rng(7))
for n in [50, 100, 200, 500, 1000, 2000, 5000]:
    res = sampler.run([(qc, None, n)] * 25).result()    # 25 repeats
    est = [r.data.meas.get_counts().get("1", 0) / n for r in res]
    if n in (50, 5000):
        print(f"shots={n}: estimates "
              f"{min(est):.3f} to {max(est):.3f}")
