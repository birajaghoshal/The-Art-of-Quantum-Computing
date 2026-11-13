# Whatever Alice does to her half of a Bell pair, Bob's qubit
# looks the same: the maximally mixed state I/2.
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, partial_trace

def bob_state(action):
    qc = QuantumCircuit(3)            # q0 Alice, q1 Bob, q2 record
    qc.h(0); qc.cx(0, 1)              # Bell pair (|00>+|11>)/sqrt 2
    if action == "rotate":
        qc.ry(0.9, 0)
    if action == "measure X":
        qc.h(0)
    if action.startswith("measure"):
        qc.cx(0, 2)                   # copy the outcome to a record
    rho = partial_trace(DensityMatrix(qc), [0, 2])    # keep q1
    return rho.data.real.round(3)

for action in ["nothing", "rotate", "measure Z", "measure X"]:
    print(f"Alice: {action:<9} Bob's matrix:",
          bob_state(action).tolist())
