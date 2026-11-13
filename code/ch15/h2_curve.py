"""Potential energy curve of H2 from tabulated Pauli coefficients."""
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

# R (angstrom), c0 (II), c1 (IZ = -ZI), c3 (ZZ), c4 (XX), E_nuc
table = [(0.35, -0.81066, 0.74742, -0.01310, 0.16257, 1.51193),
         (0.45, -0.90840, 0.63389, -0.01272, 0.16662, 1.17595),
         (0.55, -0.98051, 0.53649, -0.01230, 0.17124, 0.96214),
         (0.65, -1.02805, 0.45543, -0.01180, 0.17632, 0.81412),
         (0.735, -1.05237, 0.39794, -0.01128, 0.18093, 0.71997),
         (0.85, -1.06799, 0.33375, -0.01041, 0.18756, 0.62256),
         (1.00, -1.06924, 0.26753, -0.00901, 0.19679, 0.52918),
         (1.20, -1.05267, 0.20019, -0.00696, 0.20979, 0.44098),
         (1.50, -1.00964, 0.12910, -0.00419, 0.22954, 0.35278),
         (2.00, -0.92856, 0.06063, -0.00143, 0.25914, 0.26459),
         (2.50, -0.86072, 0.02713, -0.00038, 0.28221, 0.21167),
         (3.00, -0.81004, 0.01124, -0.00007, 0.29921, 0.17639)]
t = Parameter("t")
qc = QuantumCircuit(2)
qc.ry(t, 0)
qc.cx(0, 1)
qc.x(0)
est, x, rows = StatevectorEstimator(), [0.0], []
for R, c0, c1, c3, c4, en in table:
    H = SparsePauliOp(["II", "IZ", "ZI", "ZZ", "XX"],
                      [c0, c1, -c1, c3, c4])
    f = lambda p: float(est.run([(qc, H, p)]).result()[0].data.evs)
    res = minimize(f, x, method="COBYLA", options={"maxiter": 60})
    x = res.x                    # warm start for the next R
    exact = np.linalg.eigvalsh(H.to_matrix())[0]
    rows.append((R, f([0.0]) + en, res.fun + en, exact + en))
    print(f"R = {R:5.3f}  HF = {rows[-1][1]: .5f}  "
          f"VQE = {rows[-1][2]: .5f}  exact = {rows[-1][3]: .5f}")
R, hf, vqe, ex = np.array(rows).T
k = np.argmin(vqe)
print(f"minimum of the VQE curve: R = {R[k]} A, E = {vqe[k]:.5f} Ha")

# Plotting code for Figure 15.5: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(R, ex, "-", color="#1F5FBF", label="exact (this model)")
ax.plot(R, hf, "--", color="#F28C28", label="Hartree-Fock |01>")
ax.plot(R, vqe, "o", color="#0F9D8C", label="VQE")
ax.set_xlabel("bond length R (angstrom)")
ax.set_ylabel("total energy (Ha)")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch15/h2_curve.pdf")
