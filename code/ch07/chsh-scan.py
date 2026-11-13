# Sweep Bob's angle and plot the CHSH value S
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

def obs(label_a, angle):  # Alice's Pauli times Bob's direction
    return SparsePauliOp.from_sparse_list(
        [(label_a + "Z", [0, 1], np.cos(angle)),
         (label_a + "X", [0, 1], np.sin(angle))], 2)

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
est = StatevectorEstimator()
thetas = np.linspace(-np.pi / 2, np.pi, 61)
S = []
for t in thetas:
    ops = [obs("Z", t), obs("Z", -t), obs("X", t), obs("X", -t)]
    e = est.run([(qc, ops)]).result()[0].data.evs
    S.append(e[0] + e[1] + e[2] - e[3])

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(thetas / np.pi, S, "o-", color="#1F5FBF", ms=3,
        label="Estimator")
ax.axhline(2, color="#D64545", ls="--", label="classical bound 2")
ax.axhline(-2, color="#D64545", ls="--")
ax.axhline(2 * np.sqrt(2), color="#0F9D8C", ls=":",
           label=r"$2\sqrt{2}$")
ax.set_xlabel(r"Bob's angle $\theta/\pi$")
ax.set_ylabel("CHSH value S")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2),
          ncol=3, fontsize=8)
fig.tight_layout()
fig.savefig("figures/ch07/chsh_scan.pdf")
k = int(np.argmax(S))
print(f"largest S = {S[k]:.4f}"
      f" at theta = {thetas[k] / np.pi:.3f} pi")
