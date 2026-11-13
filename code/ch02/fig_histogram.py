# Bar chart: exact probabilities versus sampled frequencies
import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector

plt.rcParams.update({"font.size": 12})
psi = Statevector([0.6, 0.8j])
psi.seed(41)
labels = ["0", "1"]
rows = [("exact", psi.probabilities(), "#1F5FBF")]
for shots, col in [(20, "#F28C28"), (200, "#0F9D8C"),
                   (2000, "#7B4FBF")]:
    c = psi.sample_counts(shots)
    rows.append((f"{shots} shots",
                 [c.get(b, 0) / shots for b in labels], col))

fig, ax = plt.subplots(figsize=(6, 2.6))
x = np.arange(2)
w = 0.2
for i, (name, vals, col) in enumerate(rows):
    bars = ax.bar(x + (i - 1.5) * w, vals, w, label=name, color=col)
    ax.bar_label(bars, fmt="%.2f", fontsize=10, padding=1)
ax.set_xticks(x, ["outcome 0", "outcome 1"])
ax.set_ylabel("probability / frequency")
ax.set_ylim(0, 1.0)
ax.legend(ncols=4, fontsize=10, loc="upper left")
fig.tight_layout()
fig.savefig("figures/ch02/histogram.pdf", bbox_inches="tight")
print("saved figures/ch02/histogram.pdf")
