# Grover search on 2, 3 and 4 qubits with the best iteration count
import numpy as np
from qiskit.primitives import StatevectorSampler
from groverlib import grover_circuit, best_k, theory

# a Generator gives each run fresh random numbers (an int would not)
sampler = StatevectorSampler(seed=np.random.default_rng(13))
for n, target in [(2, "10"), (3, "110"), (4, "1011")]:
    k = best_k(2**n, 1)
    qc = grover_circuit(n, [target], k)
    counts = sampler.run([qc], shots=1000).result()[0].data.meas \
        .get_counts()
    top = max(counts, key=counts.get)
    print(f"n = {n}, target {target}, k = {k}: most frequent {top}, "
          f"{counts.get(target, 0)}/1000 hits "
          f"(theory {theory(2**n, 1, k):.4f})")
