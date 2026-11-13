"""Simulated Ramsey experiment: measure T2 from decaying fringes."""
import numpy as np
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit
from qiskit.circuit import Delay
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_aer.noise import RelaxationNoisePass

T1, T2 = 80e-6, 60e-6
f_det = 0.04                          # artificial detuning, MHz
relax = RelaxationNoisePass(t1s=[T1], t2s=[T2], op_types=[Delay])
sampler = AerSampler.from_backend(AerSimulator(seed_simulator=11))

waits = np.linspace(0, 120, 49)       # microseconds
circuits = []
for t in waits:
    qc = QuantumCircuit(1)
    qc.h(0)                           # put the qubit on the equator
    qc.delay(float(t), 0, unit="us")
    qc.rz(2 * np.pi * f_det * t, 0)   # phase that grows with t
    qc.h(0)
    qc.measure_all()
    circuits.append(relax(qc))
res = sampler.run(circuits, shots=1000).result()
p0 = np.array([r.data.meas.get_counts().get("0", 0) / 1000
               for r in res])

def model(t, a, t2, f, phi, b):
    return a * np.exp(-t / t2) * np.cos(2 * np.pi * f * t + phi) + b

guess = [0.5, 40, 0.035, 0, 0.5]
pars, cov = curve_fit(model, waits, p0, p0=guess)
a, t2_fit, f_fit, phi, b = pars
print(f"fitted T2        : {t2_fit:.1f} +/- {np.sqrt(cov[1,1]):.1f}"
      " us (true 60.0)")
print(f"fitted detuning  : {f_fit*1e3:.2f} kHz (set 40.00)")

# Plotting code for Figure 17.1: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(waits, p0, "o", color="#1F5FBF", ms=4,
        label="simulated data")
tt = np.linspace(0, 120, 600)
ax.plot(tt, model(tt, *pars), color="#F28C28", label="fit")
ax.plot(tt, b + a * np.exp(-tt / t2_fit), "--", color="#7B4FBF",
        label="decay envelope")
ax.set(xlabel=r"waiting time ($\mu$s)", ylabel="P(0)")
ax.grid(alpha=0.3)
ax.legend(loc="upper right")
fig.savefig("figures/ch17/ramsey_fit.pdf", bbox_inches="tight")
