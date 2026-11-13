# Watch the amplitudes during Grover search for |110> (n = 3)
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from groverlib import phase_oracle, diffuser

n, marked = 3, ["110"]
qc = QuantumCircuit(n)
qc.h(range(n))
state = Statevector(qc)
stages = [("start", state)]
for k in (1, 2):
    state = state.evolve(phase_oracle(n, marked))
    stages.append((f"oracle {k}", state))
    state = -state.evolve(diffuser(n))   # undo the diffuser's -1
    stages.append((f"diffuser {k}", state))

for name, sv in stages:
    a = np.real(sv.data)
    print(f"{name:>10}: marked {a[6]:+.4f}, others {a[0]:+.4f}, "
          f"mean {a.mean():+.4f}, P(110) = {a[6]**2:.4f}")

fig, axes = plt.subplots(1, 5, figsize=(6.4, 2.2), sharey=True)
for ax, (name, sv) in zip(axes, stages):
    a = np.real(sv.data)
    colours = ["#D64545" if i == 6 else "#1F5FBF" for i in range(8)]
    ax.bar(range(8), a, color=colours)
    ax.axhline(a.mean(), color="#F28C28", ls="--", lw=1)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_title(name, fontsize=10)
    ax.set_xticks([0, 6], ["000", "110"], fontsize=9)
axes[0].set_ylabel("amplitude")
fig.tight_layout()
fig.savefig("figures/ch13/amplitudes.pdf")
