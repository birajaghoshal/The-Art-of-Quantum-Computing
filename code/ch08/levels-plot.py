# Plot depth and CZ count against optimization level (3 seeds)
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(6)
qc.append(QFTGate(6), range(6))
qc.measure_all()
backend = FakeFez()
depth, cz = np.zeros((4, 3)), np.zeros((4, 3))
for level in range(4):
    for j, seed in enumerate([11, 12, 13]):
        pm = generate_preset_pass_manager(optimization_level=level,
                                          backend=backend,
                                          seed_transpiler=seed)
        isa = pm.run(qc)
        depth[level, j] = isa.depth()
        cz[level, j] = isa.count_ops()["cz"]

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
x = np.arange(4)
for data, lab, col, dx in [(depth, "depth", "#1F5FBF", -0.18),
                           (cz, "CZ count", "#F28C28", 0.18)]:
    m = data.mean(1)               # error bars span min to max
    ax.bar(x + dx, m, 0.36, color=col, label=lab, capsize=3,
           yerr=[m - data.min(1), data.max(1) - m])
ax.set_xticks(x)
ax.set_xlabel("optimization_level")
ax.set_ylabel("count")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch08/levels.pdf")
print("mean depth per level:", depth.mean(1).round(1))
print("mean CZ per level:   ", cz.mean(1).round(1))
