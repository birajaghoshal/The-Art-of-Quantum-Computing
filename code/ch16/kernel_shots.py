"""Estimate a kernel entry with shots: the compute-uncompute test."""
import numpy as np
from qiskit.circuit.library import zz_feature_map
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector

fmap = zz_feature_map(2, reps=2)
a, b = np.array([0.4, 1.2]), np.array([0.7, 0.9])
exact = abs(Statevector(fmap.assign_parameters(a)).inner(
    Statevector(fmap.assign_parameters(b)))) ** 2

# U(b)^dagger U(a)|00>: P(00) equals |<phi(b)|phi(a)>|^2
qc = fmap.assign_parameters(a)
qc.compose(fmap.assign_parameters(b).inverse(), inplace=True)
qc.measure_all()
sampler = StatevectorSampler(seed=np.random.default_rng(11))
print(f"exact kernel value: {exact:.4f}")
for shots in [100, 1000, 10000]:
    counts = sampler.run([qc], shots=shots).result()[0] \
        .data.meas.get_counts()
    est = counts.get("00", 0) / shots
    err = np.sqrt(est * (1 - est) / shots)
    print(f"shots = {shots:5d}: estimate {est:.4f} +/- {err:.4f}")
