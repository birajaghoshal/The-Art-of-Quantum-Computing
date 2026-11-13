"""VQE for H2 with two ansatze; energy versus iteration."""
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.circuit.library import real_amplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator

H = SparsePauliOp.from_list([
    ("II", -1.052373), ("IZ", 0.397937), ("ZI", -0.397937),
    ("ZZ", -0.011280), ("XX", 0.180931)])
E_nuc = 0.719969
exact = np.linalg.eigvalsh(H.to_matrix())[0] + E_nuc
est = StatevectorEstimator()

# Ansatz A: hardware-efficient, four parameters
hea = real_amplitudes(2, reps=1)
# Ansatz B: one parameter, cos(t/2)|01> + sin(t/2)|10>
t = Parameter("t")
chem = QuantumCircuit(2)
chem.ry(t, 0)
chem.cx(0, 1)
chem.x(0)

histories = {}                       # name -> energy at each call
for name, qc in [("real_amplitudes (4 par.)", hea),
                 ("one-parameter ansatz", chem)]:
    hist = []
    def cost(x):
        e = float(est.run([(qc, H, x)]).result()[0].data.evs)
        hist.append(e + E_nuc)
        return e
    res = minimize(cost, np.zeros(qc.num_parameters),
                   method="COBYLA", options={"maxiter": 100})
    err = abs(res.fun + E_nuc - exact)
    print(f"{name}: E = {res.fun + E_nuc:.6f} Ha")
    print(f"  error = {err:.1e} Ha, energy calls = {len(hist)}")
    print("  optimal parameters:", np.round(res.x, 4))
    histories[name] = hist

# Plotting code for Figure 15.4: see the companion repository.
import matplotlib.pyplot as plt
colours = ["#1F5FBF", "#0F9D8C"]
fig, ax = plt.subplots(figsize=(6, 3.6))
for (name, hist), col in zip(histories.items(), colours):
    ax.semilogy(np.array(hist) - exact, color=col, label=name)
ax.axhline(0.0016, ls="--", color="#D64545",
           label="chemical accuracy (1.6 mHa)")
ax.set_xlabel("energy evaluation")
ax.set_ylabel("error E - E_exact (Ha)")
ax.legend()
fig.tight_layout()
fig.savefig("figures/ch15/h2_vqe.pdf")
