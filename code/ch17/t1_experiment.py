"""Simulated T1 experiment: excite, wait, measure, fit."""
import numpy as np
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit
from qiskit.circuit import Delay
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (NoiseModel, ReadoutError,
                              RelaxationNoisePass)
from qiskit_aer.primitives import SamplerV2 as AerSampler

T1, T2 = 80e-6, 60e-6                   # the "true" device values
relax = RelaxationNoisePass(t1s=[T1], t2s=[T2], op_types=[Delay])
readout = NoiseModel()
readout.add_all_qubit_readout_error(ReadoutError([[0.97, 0.03],
                                                  [0.04, 0.96]]))
sampler = AerSampler.from_backend(
    AerSimulator(noise_model=readout, seed_simulator=7))

waits = np.linspace(0, 300, 16)         # microseconds
circuits = []
for t in waits:
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.delay(float(t), 0, unit="us")
    qc.measure_all()
    circuits.append(relax(qc))          # thermal relaxation on delay
res = sampler.run(circuits, shots=2000).result()
p1 = np.array([r.data.meas.get_counts().get("1", 0) / 2000
               for r in res])

def model(t, a, t1, b):
    return a * np.exp(-t / t1) + b

(a, t1_fit, b), cov = curve_fit(model, waits, p1, p0=[1, 50, 0])
err = np.sqrt(cov[1, 1])
for t, p in list(zip(waits, p1))[::3]:
    print(f"wait {t:5.0f} us: P(1) = {p:.4f}")
print(f"fitted T1        : {t1_fit:.1f} +/- {err:.1f} us"
      " (true 80.0)")
print(f"fitted a, b      : {a:.3f}, {b:.3f}")
