# Tomography-lite: estimate Bob's Bloch vector from X, Y and Z
# measurements, on an ideal and a noisy (FakeFez) simulator.
import numpy as np
from qiskit import ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit.transpiler import generate_preset_pass_manager
from teleport_dynamic import teleport, theta, phi

def bob_in(basis):
    qc = teleport()
    bob = ClassicalRegister(1, "bob")
    qc.add_register(bob)
    if basis == "X":
        qc.h(2)
    if basis == "Y":
        qc.sdg(2); qc.h(2)
    qc.measure(2, bob[0])
    return qc

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
noisy = AerSimulator.from_backend(backend, seed_simulator=1234)
exact = [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi),
         np.cos(theta)]
results = {"exact": exact}
for name, sim in [("ideal", AerSimulator(seed_simulator=5)),
                  ("noisy", noisy)]:
    circs = pm.run([bob_in(b) for b in "XYZ"])
    res = AerSampler.from_backend(sim).run(circs,
                                           shots=2000).result()
    r = [1 - 2 * p.data.bob.get_counts().get("1", 0) / 2000
         for p in res]                # <P> = P(0) - P(1)
    results[name] = r
    fid = (1 + np.dot(r, exact)) / 2  # estimated fidelity with input
    print(f"{name}: Bloch = ({r[0]:+.3f}, {r[1]:+.3f}, {r[2]:+.3f})"
          f"  length={np.linalg.norm(r):.3f}  F={fid:.3f}")
print(f"exact: Bloch = ({exact[0]:+.3f}, {exact[1]:+.3f}, "
      f"{exact[2]:+.3f})")

# Plotting code for Figure 14.3: see the companion repository.
import matplotlib.pyplot as plt
plt.rcParams["font.size"] = 10
fig, ax = plt.subplots(figsize=(6, 3.4))
colours = {"exact": "#5B6B7F", "ideal": "#1F5FBF",
           "noisy": "#F28C28"}
for k, (name, r) in enumerate(results.items()):
    ax.bar(np.arange(3) + (k - 1) * 0.26, r, 0.26, label=name,
           color=colours[name])
ax.set_xticks(range(3), ["<X>", "<Y>", "<Z>"])
ax.set_ylabel("Bloch component of Bob's qubit")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch14/teleport_bloch.pdf")
