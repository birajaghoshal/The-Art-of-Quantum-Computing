"""Distribution of T1 and T2 over all qubits of FakeFez."""
import matplotlib.pyplot as plt
import numpy as np
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
props = [backend.qubit_properties(q)
         for q in range(backend.num_qubits)]
t1 = np.array([p.t1 for p in props]) * 1e6        # microseconds
t2 = np.array([p.t2 for p in props]) * 1e6

for name, data in (("T1", t1), ("T2", t2)):
    print(f"{name} (us): min {data.min():6.1f}   median "
          f"{np.median(data):6.1f}   max {data.max():6.1f}")
print("Qubits with T2 > T1:", int((t2 > t1).sum()), "of", len(props))

plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(6, 3.6))
bins = np.arange(0, 350, 25)    # last edge above the largest T2
kw = dict(bins=bins, histtype="step", linewidth=1.8)
ax.hist(t1, color="#1F5FBF", label="$T_1$", **kw)
ax.hist(t2, color="#F28C28", label="$T_2$", **kw)
ax.set(xlabel="time ($\\mu$s)", ylabel="number of qubits")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch04/coherence_hist.pdf")
