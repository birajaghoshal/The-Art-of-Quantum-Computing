# A measurement in the middle of a circuit changes what follows
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

q = QuantumRegister(1, "q")
mid = ClassicalRegister(1, "mid")
end = ClassicalRegister(1, "end")

plain = QuantumCircuit(q, end)
plain.h(0)
plain.h(0)                        # H H = I, so always 0
plain.measure(0, end[0])

peek = QuantumCircuit(q, mid, end)
peek.h(0)
peek.measure(0, mid[0])           # mid-circuit measurement
peek.h(0)
peek.measure(0, end[0])

sampler = AerSampler.from_backend(AerSimulator(seed_simulator=42))
res = sampler.run([plain, peek], shots=1000).result()
print("No peek, end:  ", res[0].data.end.get_counts())
for name in ("mid", "end"):
    counts = getattr(res[1].data, name).get_counts()
    print(f"With peek, {name}:", dict(sorted(counts.items())))
