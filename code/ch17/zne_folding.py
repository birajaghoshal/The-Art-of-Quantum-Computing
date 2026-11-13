"""Zero-noise extrapolation with global folding, built by hand."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_aer.primitives import SamplerV2 as AerSampler

u = QuantumCircuit(4)                    # the circuit U to protect
for layer in range(3):
    u.ry(0.3, range(4))
    for q in range(3):
        u.cx(q, q + 1)
    u.rz(0.5, range(4))
ideal = Statevector(u).expectation_value(SparsePauliOp("ZZZZ")).real

def fold(circ, k):
    """Return U (U^dagger U)^k; barriers stop any cancellation."""
    out = circ.copy()
    for _ in range(k):
        out.barrier()
        out.compose(circ.inverse(), inplace=True)
        out.barrier()
        out.compose(circ, inplace=True)
    out.measure_all()
    return out

noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(0.02, 2),
                                  ["cx"])
noise.add_all_qubit_quantum_error(depolarizing_error(0.002, 1),
                                  ["ry", "rz"])
sampler = AerSampler.from_backend(
    AerSimulator(noise_model=noise, seed_simulator=99))
scales = np.array([1, 3, 5, 7])          # noise factor = 2k + 1
circs = [fold(u, (s - 1) // 2) for s in scales]
res = sampler.run(circs, shots=20000).result()

def parity(counts):                       # <ZZZZ> from bitstrings
    tot = sum(counts.values())
    return sum((-1) ** b.count("1") * n
               for b, n in counts.items()) / tot

vals = np.array([parity(r.data.meas.get_counts()) for r in res])
for s, c, v in zip(scales, circs, vals):
    print(f"scale {s}: {c.count_ops()['cx']:3d} CX gates, "
          f"<ZZZZ> = {v:.4f}")
fits = {"linear, 1-3": np.polyfit(scales[:2], vals[:2], 1),
        "quadratic, 1-5": np.polyfit(scales[:3], vals[:3], 2)}
b_exp = np.polyfit(scales, np.log(vals), 1)  # log-linear fit
print(f"ideal value         : {ideal:.4f}")
print(f"unmitigated         : {vals[0]:.4f}")
for name, f in fits.items():
    print(f"ZNE {name:16s}: {np.polyval(f, 0):.4f}")
print(f"ZNE exponential, 1-7: {np.exp(np.polyval(b_exp, 0)):.4f}")

# Plotting code for Figure 17.2: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.6))
x = np.linspace(0, 7.3, 200)
curves = [np.polyval(f, x) for f in fits.values()]
curves.append(np.exp(np.polyval(b_exp, x)))
for y, name, col, ls in zip(curves, ["linear", "quadratic", "exp."],
                            ["#F28C28", "#0F9D8C", "#7B4FBF"],
                            ["-", "--", ":"]):
    ax.plot(x, y, ls, color=col, lw=1.6, label=f"{name} fit")
ax.plot(scales, vals, "o", color="#1F5FBF", label="noisy data")
ax.plot(0, ideal, "*", color="#D64545", ms=13, label="ideal value")
ax.set(xlabel=r"noise scale factor $\lambda$", ylabel="<ZZZZ>")
ax.legend(fontsize=8)
fig.savefig("figures/ch17/zne_fit.pdf", bbox_inches="tight")
