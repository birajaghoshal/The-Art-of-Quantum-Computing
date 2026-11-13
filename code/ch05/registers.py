# Named registers: measure only the qubits you care about.
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler

data = QuantumRegister(2, "data")
helper = QuantumRegister(1, "helper")
result = ClassicalRegister(2, "result")
qc = QuantumCircuit(data, helper, result)

qc.x(data[0])                # data qubit 0 -> 1
qc.h(helper[0])              # helper is busy but never measured
qc.measure(data, result)     # data[i] -> result[i]
print(qc.draw("text", fold=68))

sampler = StatevectorSampler(seed=7)
pub_result = sampler.run([qc], shots=500).result()[0]
counts = pub_result.data.result.get_counts()  # register 'result'
print("counts:", dict(sorted(counts.items())))
