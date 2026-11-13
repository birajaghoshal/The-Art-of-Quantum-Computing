# A CNOT "copier" copies |0> and |1> perfectly, but not |+>
import numpy as np
from qiskit.circuit.library import CXGate
from qiskit.quantum_info import Statevector, Operator, state_fidelity

# Control = qubit 0 (the input), target = qubit 1 (the blank)
CX = Operator(CXGate())
blank = Statevector([1, 0])
s = 1 / np.sqrt(2)
inputs = {"|0>": [1, 0], "|1>": [0, 1], "|+>": [s, s],
          "0.6|0>+0.8|1>": [0.6, 0.8]}
for name, amps in inputs.items():
    psi = Statevector(amps)
    out = blank.tensor(psi).evolve(CX)   # input on q0, blank on q1
    want = psi.tensor(psi)               # a perfect copy
    f = state_fidelity(out, want)
    print(f"{name:14s} out = {np.round(out.data.real, 3)}")
    print(f"{'':14s} fidelity with a perfect copy = {f:.4f}")
