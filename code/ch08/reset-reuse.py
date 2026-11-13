# Qubit reuse: two parity checks with one recycled ancilla
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

data = QuantumRegister(3, "data")
anc = QuantumRegister(1, "anc")
syn = ClassicalRegister(2, "syn")
qc = QuantumCircuit(data, anc, syn)
qc.x(data[2])                       # data = |100>: q2 differs

for k, (i, j) in enumerate([(0, 1), (1, 2)]):
    qc.cx(data[i], anc[0])          # ancilla collects q_i XOR q_j
    qc.cx(data[j], anc[0])
    qc.measure(anc[0], syn[k])
    qc.reset(anc[0])                # recycle the ancilla

sampler = AerSampler.from_backend(AerSimulator(seed_simulator=3))
res = sampler.run([qc], shots=500).result()[0]
print("Syndrome (s1 s0):", res.data.syn.get_counts())
print("Qubits used:", qc.num_qubits, "instead of", qc.num_qubits + 1)

# Active reset: measure, then flip only if the result was 1
act = QuantumCircuit(1, 2)
act.h(0)
act.measure(0, 0)
with act.if_test((act.clbits[0], 1)):
    act.x(0)
act.measure(0, 1)
counts = (sampler.run([act], shots=500).result()[0]
          .data.c.get_counts())
print("Active reset (after, before):", dict(sorted(counts.items())))
