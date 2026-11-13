# Hadamards on both qubits swap the roles of control and target
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

sandwich = QuantumCircuit(2)
sandwich.h([0, 1])
sandwich.cx(0, 1)                # control q0, target q1 ...
sandwich.h([0, 1])

flipped = QuantumCircuit(2)
flipped.cx(1, 0)                 # ... acts as control q1, target q0

original = QuantumCircuit(2)
original.cx(0, 1)

U = Operator(sandwich)
print("Sandwich equals CX(1,0):", U.equiv(Operator(flipped)))
print("Sandwich equals CX(0,1):", U.equiv(Operator(original)))
