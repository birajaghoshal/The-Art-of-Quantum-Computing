# Chi-square goodness-of-fit test for a whole distribution.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
from scipy.stats import chisquare

def build(angle):
    qc = QuantumCircuit(3)
    qc.h(0); qc.cx(0, 1); qc.ry(angle, 2)
    return qc

expected = Statevector(build(np.pi / 3)).probabilities_dict()
keys = sorted(str(k) for k, p in expected.items() if p > 1e-12)
rng = np.random.default_rng(99)          # one stream for both runs
sampler, shots = StatevectorSampler(seed=rng), 2000
for label, angle in [("correct", np.pi / 3), ("bug", 2 * np.pi / 3)]:
    qc = build(angle)
    qc.measure_all()
    counts = sampler.run([qc], shots=shots).result()[0]\
        .data.meas.get_counts()
    stray = sum(v for k, v in counts.items() if k not in keys)
    obs = [counts.get(k, 0) for k in keys]
    stat, pval = chisquare(obs, [shots * expected[k] for k in keys])
    shown = f"= {pval:.3g}" if pval > 1e-300 else "< 1e-300"
    print(f"{label:<8} {keys} -> {obs}, stray={stray}")
    print(f"         chi2={stat:.2f}  p-value {shown}")
