"""The angle-encoding kernel is a simple classical formula."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from moons_data import load
from fidelity_kernel import feature_states, kernel

x = ParameterVector("x", 2)
angle_map = QuantumCircuit(2)
angle_map.ry(x[0], 0)
angle_map.ry(x[1], 1)
Xtr, Xte, ytr, yte = load()

K_quantum = kernel(*[feature_states(angle_map, Xtr)] * 2)
# Closed form: product over features of cos^2((x_i - x'_i) / 2)
diff = Xtr[:, None, :] - Xtr[None, :, :]
K_formula = np.prod(np.cos(diff / 2) ** 2, axis=2)
print("kernel matrix size:", K_quantum.shape)
err = np.abs(K_quantum - K_formula).max()
print(f"largest difference: {err:.1e}")
