# P(1) after RX(theta) and after RZ(theta), theta from 0 to 4 pi.
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler

theta = Parameter("θ")
circs = {}
for name in ["rx", "rz"]:
    qc = QuantumCircuit(1)
    getattr(qc, name)(theta, 0)
    qc.measure_all()
    circs[name] = qc

angles = np.linspace(0, 4 * np.pi, 33)
shots = 400
sampler = StatevectorSampler(seed=np.random.default_rng(21))
res = sampler.run([(circs["rx"], angles), (circs["rz"], angles)],
                  shots=shots).result()
p1 = {name: np.array([r.data.meas.get_counts(i).get("1", 0) / shots
                      for i in range(len(angles))])
      for name, r in zip(["rx", "rz"], res)}
for i in [0, 3, 8, 13, 24, 30]:
    print(f"θ = {angles[i]:6.3f}  RX: P(1) = {p1['rx'][i]:.3f}"
          f"  theory {np.sin(angles[i] / 2) ** 2:.3f}"
          f"   RZ: P(1) = {p1['rz'][i]:.3f}")

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
fine = np.linspace(0, 4 * np.pi, 300)
ax.plot(fine, np.sin(fine / 2) ** 2, color="#5B6B7F", lw=1,
        label=r"$\sin^2(\theta/2)$")
ax.plot(angles, p1["rx"], "o", color="#1F5FBF", ms=4,
        label="RX, sampled")
ax.plot(angles, p1["rz"], "s", color="#F28C28", ms=4,
        label="RZ, sampled")
ax.set_xticks(np.arange(5) * np.pi,
              ["0", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"])
ax.set_xlabel(r"rotation angle $\theta$")
ax.set_ylabel("P(1)")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)
fig.tight_layout()
fig.savefig("figures/ch06/rx-sweep.pdf")
print("saved figures/ch06/rx-sweep.pdf")
