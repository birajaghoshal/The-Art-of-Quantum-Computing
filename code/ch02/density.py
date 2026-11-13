# A superposition and a coin-flip mixture: tell them apart
import numpy as np
from qiskit.quantum_info import (DensityMatrix, Statevector,
                                 Operator, partial_trace)

H = Operator(np.array([[1, 1], [1, -1]]) / np.sqrt(2))
plus = DensityMatrix(Statevector([1, 1]) / np.sqrt(2))
mix = (0.5 * DensityMatrix.from_label("0")
       + 0.5 * DensityMatrix.from_label("1"))

for name, rho in [("pure |+>", plus), ("50/50 mixture", mix)]:
    print(name)
    print("  rho          :", np.round(rho.data.real, 4).tolist())
    print("  Z-basis probs:", np.round(rho.probabilities(), 4))
    px = rho.evolve(H).probabilities()
    print("  X-basis probs:", np.round(px, 4))
    print(f"  purity       : {rho.purity().real:.4f}")

# One half of a Bell pair, viewed on its own
bell = DensityMatrix(Statevector([1, 0, 0, 1]) / np.sqrt(2))
half = partial_trace(bell, [1])         # trace out qubit 1
print("Bell, qubit 0 alone:", np.round(half.data.real, 4).tolist(),
      f" purity {half.purity().real:.4f}")
