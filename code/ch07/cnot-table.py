# Truth table and matrix of CX with control q0 and target q1
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

cx = QuantumCircuit(2)
cx.cx(0, 1)                      # control = q0, target = q1

print("input (q1 q0) -> output (q1 q0)")
for label in ["00", "01", "10", "11"]:
    out = Statevector.from_label(label).evolve(cx)
    probs = out.probabilities_dict()
    result = max(probs, key=probs.get)   # most likely outcome
    print(f"     {label}      ->      {result}")

cx_eq = np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
print("Matrix equals Equation (7.3):",
      np.array_equal(Operator(cx).data.real, cx_eq))
