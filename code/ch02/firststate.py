# A qubit state as a Qiskit Statevector
import numpy as np
from qiskit.quantum_info import Statevector

psi = Statevector([0.6, 0.8j])          # amplitudes of |0> and |1>
print("amplitudes      :", np.round(psi.data, 4))
print("valid state?    :", psi.is_valid())
print("probabilities   :", np.round(psi.probabilities(), 4))

bad = Statevector([1, 1])               # forgot to normalise
print("[1, 1] valid?   :", bad.is_valid())
good = Statevector(np.array([1, 1]) / np.sqrt(2))
print("[1, 1]/sqrt(2)? :", good.is_valid())

# Global phase: multiply every amplitude by the same e^{0.9 i}
psi2 = Statevector(np.exp(0.9j) * psi.data)
print("psi2 amplitudes :", np.round(psi2.data, 4))
print("psi2 probs      :", np.round(psi2.probabilities(), 4))
print("psi == psi2     :", psi == psi2)
print("psi.equiv(psi2) :", psi.equiv(psi2))
