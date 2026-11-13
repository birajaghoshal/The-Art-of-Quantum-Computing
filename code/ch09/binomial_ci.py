# Is the measured P(1) consistent with the prediction?
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from scipy.stats import binomtest

theta, shots = 1.2, 1000
p_pred = np.sin(theta / 2) ** 2          # RY(theta): sin^2(theta/2)
sampler = StatevectorSampler(seed=np.random.default_rng(2024))
print(f"Predicted P(1) = {p_pred:.4f}")
for label, angle in [("correct", theta), ("bug (/2)", theta / 2)]:
    qc = QuantumCircuit(1)
    qc.ry(angle, 0)
    qc.measure_all()
    res = sampler.run([qc], shots=shots).result()[0]
    k = res.data.meas.get_counts().get("1", 0)
    ci = binomtest(k, shots).proportion_ci(0.95, method="wilson")
    ok = ci.low <= p_pred <= ci.high
    print(f"{label:<9} p_hat={k/shots:.3f}  "
          f"CI=[{ci.low:.3f}, {ci.high:.3f}]  "
          f"{'PASS' if ok else 'FAIL'}")
