# What lives inside a Sampler result: the BitArray.
from math import pi
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.h(0)
qc.x(1)
qc.ry(2 * pi / 3, 2)
qc.measure_all()

sampler = StatevectorSampler(seed=3)
pub_result = sampler.run([qc], shots=8).result()[0]
bits = pub_result.data.meas
print("register names:", list(pub_result.data.keys()))
print("num_bits:", bits.num_bits, " num_shots:", bits.num_shots)
print("shot by shot:", bits.get_bitstrings())
print("as integers: ", dict(sorted(bits.get_int_counts().items())))

only_q2 = bits.slice_bits([2])          # keep qubit 2 only
print("qubit 2 alone:", dict(sorted(only_q2.get_counts().items())))
low_two = bits.slice_bits([0, 1])       # qubits 1 and 0
print("qubits 1,0:   ", dict(sorted(low_two.get_counts().items())))
