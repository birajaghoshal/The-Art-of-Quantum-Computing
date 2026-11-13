import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.quantum_info import Statevector

def qpe_probs(theta, t):
    """Exact outcome probabilities of the counting register."""
    qc = QuantumCircuit(t + 1)
    qc.x(t)
    qc.h(range(t))
    for k in range(t):
        qc.cp(2 ** k * 2 * np.pi * theta, k, t)
    qc.append(QFTGate(t).inverse(), range(t))
    return Statevector(qc).probabilities(qargs=list(range(t)))

theta = 0.36                              # no short binary expansion
p5 = qpe_probs(theta, 5)
print(f"t = 5: 2^t * theta = {32 * theta:.2f}")
for m in np.argsort(p5)[::-1][:4]:
    print(f"  m = {m:2d} ({m:05b})  m/32 = {m / 32:.4f}"
          f"  P = {p5[m]:.4f}")

ts = list(range(1, 10))
best, two = [], []
print(" t  best m/2^t   P(best)  P(two nearest)")
for t in ts:
    p = qpe_probs(theta, t)
    lo = int(np.floor(2 ** t * theta)) % 2 ** t
    hi = (lo + 1) % 2 ** t
    m = lo if p[lo] >= p[hi] else hi
    best.append(p[m]); two.append(p[lo] + p[hi])
    print(f"{t:2d}  {m / 2 ** t:.4f}      {p[m]:.3f}"
          f"    {p[lo] + p[hi]:.3f}")

fig, ax = plt.subplots(1, 2, figsize=(6.4, 3.0))
ax[0].bar(range(32), p5, color="#1F5FBF")
ax[0].axvline(32 * theta, color="#D64545", ls="--", lw=1)
ax[0].set_xlabel("outcome $m$ ($t=5$)")
ax[0].set_ylabel("probability")
ax[1].plot(ts, best, "o-", color="#1F5FBF", label="nearest $m$")
ax[1].plot(ts, two, "s-", color="#0F9D8C", label="two nearest")
ax[1].axhline(4 / np.pi ** 2, color="#F28C28", ls=":",
              label=r"$4/\pi^2$")
ax[1].axhline(8 / np.pi ** 2, color="#7B4FBF", ls=":",
              label=r"$8/\pi^2$")
ax[1].set_xlabel("counting qubits $t$"); ax[1].set_ylabel("probability"); ax[1].set_ylim(0, 1.05)
ax[1].legend(fontsize=8, loc="lower right")
fig.tight_layout(); fig.savefig("figures/ch11/qpe_nonexact.pdf")
