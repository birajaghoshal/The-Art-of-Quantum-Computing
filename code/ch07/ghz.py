# GHZ states: a chain of CNOTs versus a doubling "tree"
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def ghz_chain(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    for k in range(n - 1):
        qc.cx(k, k + 1)          # each qubit copies its neighbour
    return qc

def ghz_tree(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    done = 1                     # qubits already in the GHZ state
    while done < n:
        for k in range(min(done, n - done)):
            qc.cx(k, done + k)   # every member recruits one more
        done *= 2
    return qc

print(" n  chain depth  tree depth  same state?")
for n in [3, 4, 8, 16]:
    a, b = ghz_chain(n), ghz_tree(n)
    same = Statevector(a).equiv(Statevector(b))
    print(f"{n:2d}  {a.depth():11d}  {b.depth():10d}  {same}")

amps = Statevector(ghz_tree(4)).to_dict()
print("Nonzero amplitudes for n = 4:",
      {str(k): round(float(abs(v)), 3) for k, v in amps.items()})
