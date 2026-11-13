"""How quickly does the Trotter error shrink with more steps?"""
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.synthesis import LieTrotter, SuzukiTrotter
from tfim_model import H, n, exact_state

T = 2.5
target = Statevector(exact_state(T))
reps = np.arange(1, 13)
errors = {"Lie-Trotter (order 1)": [],
          "Suzuki-Trotter (order 2)": []}
costs = {name: [] for name in errors}
for r in reps:
    for name, synth in [("Lie-Trotter (order 1)",
                         LieTrotter(reps=r)),
                        ("Suzuki-Trotter (order 2)",
                         SuzukiTrotter(order=2, reps=r))]:
        qc = QuantumCircuit(n)
        qc.append(PauliEvolutionGate(H, time=T, synthesis=synth),
                  range(n))
        qc = qc.decompose()             # simulate the actual gates
        infid = 1 - state_fidelity(Statevector(qc), target)
        errors[name].append(infid)
        costs[name].append(qc.count_ops()["rzz"])
        if r in (1, 6, 12):
            print(f"{name:24s} r={r:2d}: 1-F {infid:.2e}"
                  f"  RZZ gates {costs[name][-1]:3d}")
# Plotting code for Figure 18.1: see the companion repository.
plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.4))
for name, col, mk in zip(errors, ["#1F5FBF", "#F28C28"], ["o", "s"]):
    ax.loglog(costs[name], errors[name], marker=mk, color=col,
              lw=1.5, label=name)
ax.set(xlabel="number of two-qubit RZZ gates (cost)",
       ylabel="state infidelity $1-F$")
ax.set_title(f"total time t = {T}", fontsize=10)
ax.grid(alpha=0.3, which="both")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch18/trotter_error.pdf")
