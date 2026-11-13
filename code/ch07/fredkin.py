# Fredkin (controlled-SWAP) from two CNOTs and a Toffoli
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

c, x, y = 0, 1, 2                # control c swaps x and y
qc = QuantumCircuit(3)
qc.cx(y, x)
qc.ccx(c, x, y)
qc.cx(y, x)

ref = QuantumCircuit(3)
ref.cswap(c, x, y)
print("Decomposition equals Fredkin:",
      Operator(qc).equiv(Operator(ref)))

print("input (y x c) -> output (y x c)")
for label in ["010", "011", "100", "101", "111"]:
    out = Statevector.from_label(label).evolve(ref)
    probs = out.probabilities_dict()
    print(f"      {label}     ->      {max(probs, key=probs.get)}")
