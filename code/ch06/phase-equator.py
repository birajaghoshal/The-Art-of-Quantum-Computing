# Repeated T gates walk |+> around the equator in 45-degree steps.
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

xs, ys = [], []
for k in range(8):
    qc = QuantumCircuit(1)
    qc.h(0)                          # start at |+>
    for _ in range(k):
        qc.t(0)
    psi = Statevector(qc)
    x, y, z = [round(psi.expectation_value(SparsePauliOp(p)).real, 3)
               + 0.0 for p in "XYZ"]
    xs.append(x)
    ys.append(y)
    phi = np.degrees(np.arctan2(y, x)) % 360
    print(f"T^{k}|+>: x={x:+.3f} y={y:+.3f} z={z:+.3f}"
          f"  phi={phi:5.1f} deg")

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(3.6, 3.6))
t = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(t), np.sin(t), color="#5B6B7F", lw=0.8)
ax.scatter(xs, ys, color="#1F5FBF", zorder=3)
for k, (x, y) in enumerate(zip(xs, ys)):
    ax.annotate(f"$T^{k}$", (1.18 * x, 1.18 * y), ha="center",
                va="center", color="#7B4FBF")
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
ax.set_aspect("equal")
ax.set_xlabel("x"); ax.set_ylabel("y")
fig.tight_layout()
fig.savefig("figures/ch06/phase-equator.pdf")
print("saved figures/ch06/phase-equator.pdf")
