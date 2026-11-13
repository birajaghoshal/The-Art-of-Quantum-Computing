"""Draw the coupling map of FakeFez (Figure 4.3): colour and shape
each qubit by its number of neighbours, and mark pairs whose cz
gate is flagged unusable."""
import matplotlib.pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
cmap, target = backend.coupling_map, backend.target
degree = [len(cmap.neighbors(q)) for q in range(backend.num_qubits)]

def xy(q):
    # Rows of 16 qubits, then 4 'bridge' qubits joining two rows
    row, k = divmod(q, 20)
    if k < 16:
        return k, -2 * row
    above = min(cmap.neighbors(q))
    return above % 20, -2 * row - 1

fig, ax = plt.subplots(figsize=(6, 4.6))
for a, b in {tuple(sorted(e)) for e in cmap.get_edges()}:
    bad = target["cz"][(a, b)].error >= 0.5
    (x1, y1), (x2, y2) = xy(a), xy(b)
    ax.plot([x1, x2], [y1, y2],
            color="#D64545" if bad else "#B8C2CC",
            lw=2.5 if bad else 1.2, zorder=1)
# Shapes as well as colours, so a greyscale print stays readable
styles = {1: ("#F28C28", "o"), 2: ("#1F5FBF", "s"),
          3: ("#0F9D8C", "^")}
for d, (c, m) in styles.items():
    pts = [xy(q) for q in range(len(degree)) if degree[q] == d]
    ax.scatter(*zip(*pts), s=24, color=c, marker=m, zorder=2,
               label=f"degree {d}")
ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.1),
          frameon=False)
ax.set_axis_off()
fig.savefig("figures/ch04/gate_map.pdf", bbox_inches="tight")
print("saved figures/ch04/gate_map.pdf")
