"""Two-qubit H2 model at 0.735 angstrom: coefficients and energy."""
import numpy as np
from qiskit.quantum_info import SparsePauliOp

# STO-3G integrals in hartree; g = bonding, u = antibonding orbital
h_gg, h_uu = -1.2563391, -0.4718960    # one-electron energies
J_gg, J_uu = 0.6757101, 0.6985737      # same-orbital repulsion
J_gu, K_gu = 0.6645817, 0.1809312      # Coulomb and exchange
E_nuc = 0.7199690                      # proton-proton repulsion

E_gg = 2 * h_gg + J_gg                 # both electrons in g
E_uu = 2 * h_uu + J_uu                 # both electrons in u
E_gu = h_gg + h_uu + J_gu              # one in g, one in u
c0 = (E_gg + E_uu) / 4 + E_gu / 2
c1 = (E_uu - E_gg) / 4
c3 = -(E_gg + E_uu - 2 * E_gu) / 4
H = SparsePauliOp(["II", "IZ", "ZI", "ZZ", "XX"],
                  [c0, c1, -c1, c3, K_gu])
for label, c in H.to_list():
    print(f"  {label}: {c.real: .6f}")

vals, vecs = np.linalg.eigh(H.to_matrix())
E_hf = E_gg                            # Hartree-Fock state |01>
print("electronic eigenvalues:", np.round(vals, 5))
print(f"ground total energy      : {vals[0] + E_nuc:.6f} Ha")
print(f"Hartree-Fock total energy: {E_hf + E_nuc:.6f} Ha")
print(f"correlation energy       : {vals[0] - E_hf:.6f} Ha")
w = np.abs(vecs[:, 0]) ** 2            # ground-state weights
print(f"ground state: P(01) = {w[1]:.4f}, P(10) = {w[2]:.4f}")
