# Sweep <Z> and <X> against an RY angle with one Estimator call.
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

theta = Parameter("θ")
qc = QuantumCircuit(1)
qc.ry(theta, 0)

angles = np.linspace(0, 2 * np.pi, 41)
obs = [[SparsePauliOp("Z")], [SparsePauliOp("X")]]  # shape (2, 1)
values = angles.reshape(1, -1)                       # shape (1, 41)
evs = StatevectorEstimator().run([(qc, obs, values)]).result()[0]
evs = evs.data.evs                                   # shape (2, 41)
print("evs shape:", evs.shape)
print(f"θ = π/2:  <Z> = {evs[0, 10]:+.4f}  <X> = {evs[1, 10]:+.4f}")

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(angles, evs[0], color="#1F5FBF", label=r"$\langle Z\rangle$")
ax.plot(angles, evs[1], color="#F28C28", label=r"$\langle X\rangle$")
ax.set_xlabel(r"RY angle $\theta$ (radians)")
ax.set_ylabel("expectation value")
ax.axhline(0, color="#5B6B7F", lw=0.6)
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig("figures/ch05/estimator-sweep.pdf")
print("saved figures/ch05/estimator-sweep.pdf")
