# Measuring one qubit of an entangled pair
import numpy as np
from qiskit.quantum_info import Statevector

def show(d):
    return {str(k): round(float(v), 4) for k, v in sorted(d.items())}

bell = Statevector([1, 0, 0, 1]) / np.sqrt(2)  # (|00> + |11>)/sqrt2
bell.seed(5)
counts = bell.sample_counts(1000)
print("Bell, 1000 shots:",
      {str(k): int(v) for k, v in sorted(counts.items())})

r = 1 / np.sqrt(3)
psi = Statevector([r, r, 0, r])          # (|00> + |01> + |11>)/sqrt3
print("q1 before       :", show(psi.probabilities_dict([1])))
print("q0 outcomes     :", show(psi.probabilities_dict([0])))
for bit in (0, 1):
    # keep amplitudes whose index has q0 == bit, then renormalise
    keep = np.array([(k & 1) == bit for k in range(4)])
    amps = np.where(keep, psi.data, 0)
    post = Statevector(amps / np.linalg.norm(amps))
    print(f"if q0 = {bit}: state {np.round(post.data.real, 4)},"
          f" q1 {show(post.probabilities_dict([1]))}")
