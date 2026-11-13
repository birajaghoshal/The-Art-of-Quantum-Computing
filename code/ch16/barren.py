"""Gradient variance versus qubit number for random circuits."""
import numpy as np
from qiskit.circuit.library import efficient_su2
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

est, rng, S = StatevectorEstimator(), np.random.default_rng(1), 100
sizes, rows = [2, 4, 6, 8, 10], []

def grad_variance(qc, observables):
    # S random parameter draws; parameter-shift derivative, theta[0]
    P = qc.num_parameters
    theta = rng.uniform(0, 2 * np.pi, size=(S, P))
    shift = np.zeros(P)
    shift[0] = np.pi / 2
    vals = np.stack([theta + shift, theta - shift], axis=1)
    obs = [[[o]] for o in observables]       # broadcast over draws
    ev = est.run([(qc, obs, vals)]).result()[0].data.evs
    return np.var(0.5 * (ev[..., 0] - ev[..., 1]), axis=1)

for n in sizes:
    glob = SparsePauliOp("Z" * n)              # Z on every qubit
    loc = SparsePauliOp("I" * (n - 2) + "ZZ")  # Z on qubits 0 and 1
    deep = efficient_su2(n, reps=n, entanglement="linear")
    shallow = efficient_su2(n, reps=1, entanglement="linear")
    rows.append([*grad_variance(deep, [glob, loc]),
                 *grad_variance(shallow, [loc])])
rows = np.array(rows)
print(" n   global, depth n   local, depth n   local, depth 1")
for n, (a, b, c) in zip(sizes, rows):
    print(f"{n:2d}   {a:14.2e}   {b:14.2e}   {c:14.2e}")

# Plotting code for Figure 16.6: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.6))
labels = ["global cost, depth n", "local cost, depth n",
          "local cost, depth 1"]
for k, col in enumerate(["#D64545", "#1F5FBF", "#2E9E5B"]):
    ax.semilogy(sizes, rows[:, k], "o-", color=col, label=labels[k])
ax.semilogy(sizes, 0.5 * 2.0 ** -np.array(sizes), "--",
            color="#5B6B7F", label=r"$\propto 2^{-n}$")
ax.set_xlabel("number of qubits n")
ax.set_ylabel(r"Var$[\partial E / \partial \theta_0]$")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("figures/ch16/barren.pdf")
