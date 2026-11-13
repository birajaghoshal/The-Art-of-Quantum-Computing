# Check the hand-built oracle and diffuser as matrices (n = 3)
import numpy as np
from qiskit.quantum_info import Operator, Statevector
from groverlib import phase_oracle, diffuser

n, marked = 3, ["110"]
O = Operator(phase_oracle(n, marked)).data
print("oracle diagonal:", np.real(np.diag(O)).round(3))
print("oracle is diagonal:", np.allclose(O, np.diag(np.diag(O))))

# The diffuser should equal 2|s><s| - I, possibly times -1
s = Statevector.from_label("+" * n).data
reflect = 2 * np.outer(s, s.conj()) - np.eye(2**n)
D = Operator(diffuser(n))
print("diffuser equiv 2|s><s| - I:", D.equiv(Operator(reflect)))
print("exactly equal:", np.allclose(D.data, reflect),
      "| equal to minus it:", np.allclose(D.data, -reflect))
