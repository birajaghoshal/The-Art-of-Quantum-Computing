# Global phase is invisible; relative phase is not.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def probs_in_basis(psi, basis):
    """P(0), P(1) when measuring psi in the Z, X or Y basis."""
    qc = QuantumCircuit(1)
    if basis == "X":
        qc.h(0)
    if basis == "Y":
        qc.sdg(0)
        qc.h(0)
    return np.round(psi.evolve(qc).probabilities(), 3).tolist()

psi = Statevector([0.6, 0.8j])
psi_g = np.exp(0.7j) * psi              # global phase 0.7 rad
plus = Statevector.from_label("+")
minus = Statevector.from_label("-")     # relative phase pi

for basis in "ZXY":
    print(f"{basis} basis: psi {probs_in_basis(psi, basis)}"
          f"  e^(0.7i) psi {probs_in_basis(psi_g, basis)}")
print("psi == e^(0.7i) psi:", psi == psi_g,
      "  equiv:", psi.equiv(psi_g))
print()
for basis in "ZX":
    print(f"{basis} basis: |+> {probs_in_basis(plus, basis)}"
          f"  |-> {probs_in_basis(minus, basis)}")
print("|+> equiv |->:", plus.equiv(minus))
