"""Logical versus physical error rate for the bit-flip code."""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
from qiskit_aer.primitives import SamplerV2 as AerSampler

data, anc = QuantumRegister(3, "d"), QuantumRegister(2, "a")
syn, out = ClassicalRegister(2, "syn"), ClassicalRegister(3, "out")
qc = QuantumCircuit(data, anc, syn, out)
qc.id(data)                          # the only noisy step: each data
qc.cx(data[0], anc[0])               # qubit flips with probability p
qc.cx(data[1], anc[0])
qc.cx(data[1], anc[1])
qc.cx(data[2], anc[1])
qc.measure(anc, syn)
for value, target in [(1, 0), (3, 1), (2, 2)]:
    with qc.if_test((syn, value)):
        qc.x(data[target])
qc.measure(data, out)                # logical 0 is |000>

ps = np.array([0.02, 0.05, 0.1, 0.2, 0.3, 0.5])
shots, logical = 15000, []
rng = np.random.default_rng(17)     # independent seed for each p
for p in ps:
    noise = NoiseModel()
    noise.add_all_qubit_quantum_error(
        pauli_error([("X", p), ("I", 1 - p)]), ["id"])
    seed = int(rng.integers(2**31))  # a new seed for each p
    sim = AerSimulator(noise_model=noise, seed_simulator=seed)
    counts = AerSampler.from_backend(sim).run(
        [qc], shots=shots).result()[0].data.out.get_counts()
    fails = sum(n for b, n in counts.items() if b.count("1") >= 2)
    logical.append(fails / shots)
    theory = 3 * p**2 - 2 * p**3
    print(f"p = {p:.2f}: logical {fails/shots:.5f}  "
          f"(theory {theory:.5f})")

# Plotting code for Figure 17.3: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.6))
x = np.linspace(0.01, 0.5, 200)
ax.loglog(x, x, "--", color="#999999", label="no encoding ($p_L=p$)")
ax.loglog(x, 3 * x**2 - 2 * x**3, color="#F28C28",
          label="theory $3p^2-2p^3$")
ax.loglog(ps, logical, "o", color="#1F5FBF", ms=6,
          label="simulated bit-flip code")
ax.set(xlabel="physical error probability $p$",
       ylabel="logical error rate $p_L$")
ax.grid(alpha=0.3, which="both")
ax.legend()
fig.savefig("figures/ch17/bitflip_rates.pdf", bbox_inches="tight")
