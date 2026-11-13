# Which character of a bitstring belongs to which qubit?
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.x(0)          # flip qubit 0 only
qc.x(1)          # flip qubit 1 only; qubit 2 stays |0>

state = Statevector(qc)
probs = state.probabilities_dict()
print("Probabilities:", {str(k): float(v) for k, v in probs.items()})
print("Index of the nonzero amplitude:",
      int(abs(state.data).argmax()))

qc.measure_all()
sampler = StatevectorSampler(seed=7)
result = sampler.run([qc], shots=100).result()[0]
counts = result.data.meas.get_counts()
print("Counts:", dict(sorted(counts.items())))

bits = list(counts)[0]
for q in range(3):
    # character for qubit q sits at position -(q+1)
    print(f"qubit {q} reads {bits[-(q + 1)]}")
