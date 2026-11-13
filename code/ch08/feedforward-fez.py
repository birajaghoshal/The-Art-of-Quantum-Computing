# The same feed-forward circuit, compiled and run on noisy FakeFez
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

q, c = QuantumRegister(2, "q"), ClassicalRegister(2, "c")
qc = QuantumCircuit(q, c)
qc.h(0)
qc.cx(0, 1)
qc.measure(0, c[0])
with qc.if_test((c[0], 1)) as else_:
    qc.x(1)                       # q0 read 1: flip q1
with else_:
    qc.id(1)                      # q0 read 0: nothing to do
qc.measure(1, c[1])

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
print("ISA ops:", dict(isa.count_ops()))

sim = AerSimulator.from_backend(backend, seed_simulator=1234)
res = AerSampler.from_backend(sim).run([isa], shots=4000).result()[0]
counts = dict(sorted(res.data.c.get_counts().items()))
ok = sum(n for k, n in counts.items() if k[0] == "0") / 4000
print("Counts (c1 c0):", counts)
print(f"Fraction with q1 = 0: {ok:.4f}")
