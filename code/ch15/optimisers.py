"""COBYLA, SPSA and parameter-shift gradient descent compared."""
import numpy as np
from scipy.optimize import minimize
from qiskit.circuit.library import real_amplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

H = SparsePauliOp.from_list([("ZI", 0.5), ("IZ", -1.0),
                             ("XX", 0.25)])
ansatz, est = real_amplitudes(2, reps=1), StatevectorEstimator()
E = lambda X: est.run([(ansatz, H, X)]).result()[0].data.evs

def run_cobyla(x, trace):            # one circuit per call
    f = lambda x: trace.append(float(E(x))) or trace[-1]
    minimize(f, x, method="COBYLA", options={"maxiter": 60})
    return np.arange(1, len(trace) + 1)

def run_spsa(x, trace, a=0.8, c=0.2):
    rng = np.random.default_rng(1)
    for k in range(60):              # two circuits per step
        ak, ck = a / (k + 1) ** 0.602, c / (k + 1) ** 0.101
        d = rng.choice([-1, 1], size=len(x))   # random direction
        ep, em = E(np.vstack([x + ck * d, x - ck * d]))
        x = x - ak * (ep - em) / (2 * ck) * d
        trace.append(float(E(x)))    # logged for the plot only
    return 2 * np.arange(1, 61)

def run_shift(x, trace, lr=0.6):
    P = len(x)
    S = np.vstack([np.eye(P), -np.eye(P)]) * np.pi / 2
    for k in range(15):              # 2P circuits per step
        v = E(x + S)
        x = x - lr * 0.5 * (v[:P] - v[P:])
        trace.append(float(E(x)))
    return 2 * P * np.arange(1, 16)

exact = np.linalg.eigvalsh(H.to_matrix())[0]
results = {}                         # name -> (calls, energies)
for name, run in [("COBYLA", run_cobyla), ("SPSA", run_spsa),
                  ("Param-shift GD", run_shift)]:
    trace = []
    calls = run(np.full(4, 0.1), trace)
    results[name] = (calls, trace)
    print(f"{name:15s} final E = {trace[-1]: .4f} "
          f"after {calls[-1]} calls")
print(f"exact ground energy = {exact:.4f}")

# Plotting code for Figure 15.2: see the companion repository.
import matplotlib.pyplot as plt
colours = {"COBYLA": "#1F5FBF", "SPSA": "#F28C28",
           "Param-shift GD": "#0F9D8C"}
fig, ax = plt.subplots(figsize=(6, 3.6))
for name, (calls, trace) in results.items():
    ax.plot(calls, trace, label=name, color=colours[name])
ax.axhline(exact, ls="--", color="#D64545", label="exact")
ax.set_xlabel("energy evaluations (circuits run)")
ax.set_ylabel("energy")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch15/optimisers.pdf")
