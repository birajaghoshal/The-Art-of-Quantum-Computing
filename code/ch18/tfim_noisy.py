"""Capstone, part 2: noisy FakeFez runs and ZNE."""
import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez
from tfim_model import n, steps, times, mag, trotter, exact_curve

chain = [124, 123, 136, 143, 142, 141]  # from choose_qubits.py
backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, initial_layout=chain,
    seed_transpiler=11)
scales = [1, 3, 5]
circs = []
for k in range(steps + 1):              # one circuit per (t, scale)
    for lam in scales:
        qc = trotter(k, fold=(lam - 1) // 2)
        qc.measure_all()
        circs.append(pm.run(qc))
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
res = AerSampler.from_backend(sim).run(circs, shots=4000).result()

ro = np.array([backend.target["measure"][(q,)].error for q in chain])
def magnetisation(counts):
    """Mean <Z_i> from bitstrings, with simple readout correction."""
    z, tot = np.zeros(n), sum(counts.values())
    for bits, c in counts.items():
        z += c * np.array([1 - 2 * int(bits[n - 1 - i])
                           for i in range(n)])
    return np.mean(z / tot / (1 - 2 * ro))

m = np.array([magnetisation(r.data.meas.get_counts()) for r in res])
m = m.reshape(steps + 1, len(scales))   # rows: time, cols: scale
zne = np.array([np.polyval(np.polyfit(scales, row, 2), 0)
                for row in m])  # quadratic through 3 points, at 0
exact = exact_curve(times)
ideal = [Statevector(trotter(k)).expectation_value(mag).real
         for k in range(steps + 1)]
print(" t    exact   Trotter  noisy    ZNE")
for t, e, i, row, z in zip(times, exact, ideal, m, zne):
    print(f"{t:.2f}  {e:+.4f}  {i:+.4f}  {row[0]:+.4f}  {z:+.4f}")
last = [c.count_ops()["cz"] for c in circs[-3:]]
print("CZ gates in the t = 2.5 circuits (scales 1, 3, 5):", last)
for name, vals in [("noisy", m[:, 0]), ("ZNE", zne)]:
    print(f"mean |{name} - Trotter| = "
          f"{np.mean(np.abs(vals - ideal)):.4f}")
# Plotting code for Figure 18.2: see the companion repository.
plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(times, exact, "-", color="#1F5FBF", lw=2, label="exact")
ax.plot(times, ideal, "--", color="#0F9D8C", lw=1.5,
        label="ideal Trotter circuits")
ax.plot(times, m[:, 0], "s", color="#D64545", ms=5,
        label="noisy (FakeFez model)")
ax.plot(times, zne, "o", color="#F28C28", ms=7, mfc="none", mew=1.6,
        label="noisy + ZNE")
ax.set(xlabel="time $t$ (units of $1/J$)",
       ylabel=r"magnetisation $\langle m_z\rangle$")
ax.grid(alpha=0.3)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("figures/ch18/tfim_capstone.pdf")
