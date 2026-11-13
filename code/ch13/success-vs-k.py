# Success probability against iterations: n = 5, one marked item
import numpy as np
import matplotlib.pyplot as plt
from qiskit.primitives import StatevectorSampler
from groverlib import grover_circuit, theory

n, target = 5, "10110"
N = 2**n
ks = list(range(13))
circuits = [grover_circuit(n, [target], k) for k in ks]
rng = np.random.default_rng(5)   # fresh randomness for each circuit
sampler = StatevectorSampler(seed=rng)
results = sampler.run(circuits, shots=1000).result()
measured = [r.data.meas.get_counts().get(target, 0) / 1000
            for r in results]
for k in ks[::2]:                # print even k only
    print(f"k = {k:>2}: theory {theory(N, 1, k):.4f}, "
          f"measured {measured[k]:.3f}")

fine = np.linspace(0, 12, 300)
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.plot(fine, theory(N, 1, fine), color="#1F5FBF",
        label=r"$\sin^2((2k+1)\theta/2)$")
ax.plot(ks, measured, "o", color="#F28C28",
        label="simulated, 1000 shots")
ax.set_xlabel("Grover iterations k")
ax.set_ylabel("P(find 10110)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=2,
          fontsize=9)
fig.tight_layout()
fig.savefig("figures/ch13/success_vs_k.pdf")
