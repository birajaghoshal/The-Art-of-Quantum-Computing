"""Gate and readout errors across the whole device, and a rough
'error budget' for a circuit."""
import numpy as np
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
target = backend.target
n = backend.num_qubits

sx = np.array([target["sx"][(q,)].error for q in range(n)])
ro = np.array([target["measure"][(q,)].error for q in range(n)])
cz_all = np.array([p.error for p in target["cz"].values()])
bad = cz_all == 1.0            # error 1.0 marks a pair to avoid
cz = cz_all[~bad]

print(f"median sx error:      {np.median(sx):.5f}")
print(f"median cz error:      {np.median(cz):.5f}")
print(f"median readout error: {np.median(ro):.4f}")
print("cz pairs flagged unusable (directed):", int(bad.sum()))

# If every gate fails independently, success ~ (1 - error)^count
for k in (10, 100, 1000):
    p = (1 - np.median(cz)) ** k
    print(f"chance that {k:>4} median cz gates all succeed: {p:.3f}")
