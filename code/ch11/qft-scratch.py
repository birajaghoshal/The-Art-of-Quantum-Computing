import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.quantum_info import Operator

def my_qft(n, swaps=True):
    """QFT built from H, controlled phases and final swaps."""
    qc = QuantumCircuit(n, name="myQFT")
    for target in reversed(range(n)):    # most significant first
        qc.h(target)
        for ctrl in reversed(range(target)):
            angle = np.pi / 2 ** (target - ctrl)
            qc.cp(angle, ctrl, target)
    if swaps:
        for q in range(n // 2):
            qc.swap(q, n - 1 - q)        # reverse the qubit order
    return qc

n, N = 3, 8
print(my_qft(n).draw("text", fold=68))

F = np.array([[np.exp(2j * np.pi * j * k / N) for j in range(N)]
              for k in range(N)]) / np.sqrt(N)
lib = QuantumCircuit(n)
lib.append(QFTGate(n), range(n))
for nq in (2, 3, 4, 5):
    same = Operator(my_qft(nq)).equiv(Operator(QFTGate(nq)))
    print(f"n = {nq}: my QFT equals QFTGate? {same}")
print("QFTGate(3) equals DFT matrix?",
      np.allclose(Operator(lib).data, F))      # exact, no phase
print("my QFT without swaps equals F?",
      np.allclose(Operator(my_qft(n, swaps=False)).data, F))
