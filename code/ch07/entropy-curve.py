# Entropy of cos(t/2)|00> + sin(t/2)|11> as the angle t varies
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, entropy

def ent(t):
    qc = QuantumCircuit(2)
    qc.ry(t, 0)
    qc.cx(0, 1)
    rho = partial_trace(Statevector(qc), [1])   # keep q0 only
    return entropy(rho, base=2)

angles = np.linspace(0, 2 * np.pi, 81)
values = [ent(t) for t in angles]

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(angles / np.pi, values, color="#1F5FBF", lw=2)
ax.axhline(1, color="#F28C28", ls="--", label="maximum (Bell state)")
ax.set_xlabel(r"angle $\theta/\pi$")
ax.set_ylabel("entanglement entropy (bits)")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0),
          frameon=False)
fig.tight_layout()
fig.savefig("figures/ch07/entropy_curve.pdf")

for t in [0.25, 0.5, 1.0]:
    print(f"theta = {t:.2f} pi  ->  S = {ent(t * np.pi):.3f} bits")
