# A home-made histogram with error bars of one standard error.
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.h(0)
qc.x(1)
qc.ry(2 * pi / 3, 2)
qc.measure_all()
shots = 500
counts = StatevectorSampler(seed=8).run([qc], shots=shots).result()
counts = counts[0].data.meas.get_counts()

labels = [format(i, "03b") for i in range(8)]     # all 8 outcomes
p = np.array([counts.get(b, 0) / shots for b in labels])
err = np.sqrt(p * (1 - p) / shots)                 # standard error
exact = [0, 0, 0.125, 0.125, 0, 0, 0.375, 0.375]
for b, prob, e in zip(labels, p, err):
    print(f"{b}: {prob:.3f} +/- {e:.3f}")

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.bar(labels, p, yerr=err, capsize=3, color="#0F9D8C",
       label="measured (500 shots)")
ax.scatter(labels, exact, marker="D", s=30, color="#D64545",
           zorder=3, label="exact")
ax.set_xlabel(r"outcome $q_2q_1q_0$")
ax.set_ylabel("probability")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch05/own-bars.pdf")
print("saved figures/ch05/own-bars.pdf")
