from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

secret, n = "110101", 6
qc = QuantumCircuit(n + 1, n)
qc.x(n)
qc.h(range(n + 1))
for q, bit in enumerate(reversed(secret)):
    if bit == "1":
        qc.cx(q, n)
qc.h(range(n))
qc.measure(range(n), range(n))

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
ops = isa.count_ops()
print("ISA depth:", isa.depth(), " cz gates:", ops.get("cz", 0))

sim = AerSimulator.from_backend(backend, seed_simulator=1234)
res = AerSampler.from_backend(sim).run([isa], shots=2000).result()
counts = res[0].data.c.get_counts()
top = sorted(counts.items(), key=lambda kv: -kv[1])[:5]
for bits, c in top:
    print(f"{bits}  {c:5d}  {'<- secret' if bits == secret else ''}")
print(f"P(secret) = {counts.get(secret, 0) / 2000:.3f}")

