# Random Z errors (dephasing) slowly turn |+> into a mixture
import numpy as np
from qiskit.quantum_info import (DensityMatrix, Statevector,
                                 Operator, Pauli)

Z = Operator(Pauli("Z"))
plus = DensityMatrix(Statevector([1, 1]) / np.sqrt(2))
print("   p    rho_01    <X>   purity")
for p in [0.0, 0.1, 0.25, 0.4, 0.5]:
    # with probability p a Z error happens, otherwise nothing
    rho = (1 - p) * plus + p * plus.evolve(Z)
    x = rho.expectation_value(Pauli("X")).real
    print(f"{p:5.2f}  {rho.data[0, 1].real:7.4f}  {x:6.4f}"
          f"  {rho.purity().real:.4f}")
