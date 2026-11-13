"""A complete hybrid loop on one qubit: minimise <H>."""
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

H = SparsePauliOp(["Z", "X"], coeffs=[0.6, 0.8])
theta = Parameter("theta")
qc = QuantumCircuit(1)
qc.ry(theta, 0)               # trial state |psi(theta)>

est = StatevectorEstimator()
history = []

def energy(params):
    # Quantum step: estimate <psi(theta)|H|psi(theta)>
    evs = est.run([(qc, H, params)]).result()[0].data.evs
    history.append(float(evs))
    return float(evs)

# Classical step: COBYLA proposes the next theta
res = minimize(energy, x0=[0.1], method="COBYLA",
               options={"maxiter": 40})
for k in [0, 1, 2, 10, len(history) - 1]:
    print(f"call {k:2d}: E = {history[k]: .5f}")
print(f"energy calls used   : {len(history)}")
print(f"best theta (rad)    : {res.x[0]:.4f}")
exact = np.linalg.eigvalsh(H.to_matrix())[0]
print(f"exact ground energy : {exact:.5f}")
