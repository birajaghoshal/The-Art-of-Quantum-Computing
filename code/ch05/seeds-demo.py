# Seeds make random results repeatable.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

def counts_with(seed):
    sampler = StatevectorSampler(seed=seed)
    res = sampler.run([qc], shots=100).result()
    return dict(sorted(res[0].data.meas.get_counts().items()))

print("seed 42, first run: ", counts_with(42))
print("seed 42, second run:", counts_with(42))
print("seed 43:            ", counts_with(43))
