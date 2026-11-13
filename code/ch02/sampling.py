# Shots: sampling measurement outcomes from a Statevector
import numpy as np
from qiskit.quantum_info import Statevector

psi = Statevector([0.6, 0.8j])
exact = psi.probabilities_dict()
print("exact      :",
      {str(k): round(float(v), 4) for k, v in exact.items()})

psi.seed(2026)                          # reproducible random draws
print("ten shots  :", "".join(psi.sample_memory(10)))
for shots in [10, 100, 1000, 10000]:
    raw = psi.sample_counts(shots)
    counts = {str(k): int(v) for k, v in sorted(raw.items())}
    p1 = counts.get("1", 0) / shots
    se = np.sqrt(0.64 * 0.36 / shots)   # standard error, Chapter 1
    print(f"{shots:5d} shots: {str(counts):22s} P(1) ~ {p1:.4f}"
          f" +/- {se:.4f}")
