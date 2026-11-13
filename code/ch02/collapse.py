# Measurement changes the state: collapse and repeated measurement
import numpy as np
from qiskit.quantum_info import Statevector, Operator

psi = Statevector([0.6, 0.8j])
psi.seed(7)
outcome, after = psi.measure()          # one shot and the new state
print("first outcome     :", outcome)
print("state afterwards  :", np.round(after.data, 4))

after.seed(8)
again = [str(after.measure()[0]) for _ in range(10)]
print("ten more Z results:", "".join(again))

# Now measure in the X basis instead (rotate with H, then read Z)
H = Operator(np.array([[1, 1], [1, -1]]) / np.sqrt(2))
xview = after.evolve(H)
xview.seed(9)
counts = xview.sample_counts(1000)
print("X basis, 1000 shots:",
      {str(k): int(v) for k, v in sorted(counts.items())})
