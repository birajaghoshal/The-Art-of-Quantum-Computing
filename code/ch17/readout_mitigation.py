"""Readout error mitigation with a full calibration matrix."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (NoiseModel, ReadoutError,
                              depolarizing_error)
from qiskit_aer.primitives import SamplerV2 as AerSampler

n, shots = 3, 8000
noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(0.01, 2),
                                  ["cx"])
for q, (e01, e10) in enumerate([(0.02, 0.06), (0.03, 0.08),
                                 (0.01, 0.05)]):
    noise.add_readout_error(ReadoutError([[1 - e01, e01],
                                          [e10, 1 - e10]]), [q])
sampler = AerSampler.from_backend(
    AerSimulator(noise_model=noise, seed_simulator=5))

def probs(result):                     # counts -> probability vector
    vec = np.zeros(2**n)
    for bits, k in result.data.meas.get_counts().items():
        vec[int(bits, 2)] = k / shots
    return vec

# Calibration: prepare each basis state j to measure column j of A
cals = []
for j in range(2**n):
    cal = QuantumCircuit(n)
    for q in range(n):
        if (j >> q) & 1:
            cal.x(q)
    cal.measure_all()
    cals.append(cal)
ghz = QuantumCircuit(n)
ghz.h(0)
ghz.cx([0, 1], [1, 2])                 # CX(0,1) then CX(1,2)
ghz.measure_all()
# One run call, so each circuit gets its own random stream
res = sampler.run(cals + [ghz], shots=shots).result()
A = np.column_stack([probs(r) for r in res[:2**n]])
raw = probs(res[2**n])
print("calibration circuits used:", 2**n)
print("diagonal of A:", np.round(np.diag(A), 3))
mit = np.linalg.solve(A, raw)          # same as inv(A) @ raw
ideal = np.zeros(2**n)
ideal[[0, 7]] = 0.5
for name, p in [("raw", raw), ("mitigated", mit)]:
    tvd = 0.5 * np.abs(p - ideal).sum()
    print(f"{name:9s} P(000)={p[0]:.4f} P(111)={p[7]:.4f} "
          f"min={p.min():+.4f} distance={tvd:.4f}")
