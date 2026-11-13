# Two qubits: tensor products and Qiskit's bit order
import numpy as np
from qiskit.quantum_info import Statevector

def show(d):
    return {str(k): round(float(v), 4) for k, v in sorted(d.items())}

a = Statevector([0.6, 0.8])           # this one becomes qubit 1
b = Statevector([1, 1j]) / np.sqrt(2) # this one becomes qubit 0
ab = a.tensor(b)                      # a (x) b: rightmost = qubit 0
print("amplitudes  :", np.round(ab.data, 4))
print("all outcomes:", show(ab.probabilities_dict()))
print("qubit 0 only:", show(ab.probabilities_dict([0])))
print("qubit 1 only:", show(ab.probabilities_dict([1])))

# Labels are written q1 q0, so "01" means q1 = 0 and q0 = 1
print("from_label('01') amplitudes:",
      Statevector.from_label("01").data.real)
