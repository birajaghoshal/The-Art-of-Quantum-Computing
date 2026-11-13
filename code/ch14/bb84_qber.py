# QBER as a function of the fraction of qubits Eve intercepts.
import numpy as np
from bb84_sim import run_bb84

fractions = np.linspace(0, 1, 11)
qber, err = [], []
for k, f in enumerate(fractions):
    r = run_bb84(2000, eve=f, seed=100 + k)
    keep = r["a_basis"] == r["b_basis"]
    q = np.mean(r["a_bit"][keep] != r["b_bit"][keep])
    qber.append(q)
    err.append(np.sqrt(q * (1 - q) / keep.sum()))   # standard error
    if k % 5 == 0:                   # print f = 0.0, 0.5 and 1.0
        print(f"Eve intercepts {f:.1f}: sifted {keep.sum():4d}  "
              f"QBER {q:.3f}  (theory {f / 4:.3f})")

# Plotting code for Figure 14.5: see the companion repository.
import matplotlib.pyplot as plt
plt.rcParams["font.size"] = 10
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(fractions, fractions / 4, color="#F28C28",
        label="theory: f/4")
ax.errorbar(fractions, qber, yerr=err, fmt="o", color="#1F5FBF",
            capsize=3, label="simulation (2000 qubits)")
ax.set_xlabel("fraction f of qubits intercepted by Eve")
ax.set_ylabel("QBER on the sifted key")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch14/bb84_qber.pdf")
