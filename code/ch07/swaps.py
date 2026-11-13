# SWAP from three CNOTs, and a look at iSWAP
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import iSwapGate
from qiskit.quantum_info import Operator

three = QuantumCircuit(2)
three.cx(0, 1)
three.cx(1, 0)
three.cx(0, 1)
swap = QuantumCircuit(2)
swap.swap(0, 1)
print("CX CX CX equals SWAP:", Operator(three).equiv(Operator(swap)))

print("iSWAP matrix:")
print(Operator(iSwapGate()).data.round(3))

# iSWAP = SWAP, then CZ, then S on each qubit
built = QuantumCircuit(2)
built.swap(0, 1)
built.cz(0, 1)
built.s([0, 1])
print("SWAP + CZ + S.S equals iSWAP:",
      Operator(built).equiv(Operator(iSwapGate())))
