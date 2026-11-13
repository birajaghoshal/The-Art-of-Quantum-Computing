"""Inspect the ZZ feature map for two features."""
import numpy as np
from qiskit.circuit.library import zz_feature_map
from qiskit.quantum_info import Statevector

fmap = zz_feature_map(2, reps=2)
print("parameters:", [p.name for p in fmap.parameters])
print("gate counts:", dict(fmap.count_ops()))

x = np.array([0.4, 1.9])
state = Statevector(fmap.assign_parameters(x))
print("amplitudes for x = (0.4, 1.9):")
for k, a in enumerate(state.data):
    print(f"  |{k:02b}>: {a.real:+.4f} {a.imag:+.4f}i")
# The entangling phase uses phi(x0, x1) = (pi - x0)(pi - x1)
print(f"phi(x0, x1) = {(np.pi - x[0]) * (np.pi - x[1]):.4f}")

fig = zz_feature_map(2, reps=1).draw("mpl")
fig.savefig("figures/ch16/zz_map.pdf", bbox_inches="tight")
