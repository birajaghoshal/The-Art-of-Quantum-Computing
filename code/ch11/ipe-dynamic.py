import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

theta, m = 13 / 16, 4                     # 13/16 = 0.1101 in binary
phi = 2 * np.pi * theta
anc, tgt = QuantumRegister(1, "a"), QuantumRegister(1, "t")
c = ClassicalRegister(m, "c")             # c[m-k] stores bit theta_k
qc = QuantumCircuit(anc, tgt, c)
qc.x(tgt)                                 # eigenstate |1> of P(phi)

for k in range(m, 0, -1):                 # lowest bit first
    if k < m:
        qc.reset(anc)                     # reuse the single ancilla
    qc.h(anc)
    qc.cp(2 ** (k - 1) * phi, anc[0], tgt[0])
    for j in range(k + 1, m + 1):         # feed-forward corrections
        with qc.if_test((c[m - j], 1)):
            qc.p(-np.pi / 2 ** (j - k), anc)
    qc.h(anc)
    qc.measure(anc, c[m - k])

sim = AerSimulator(seed_simulator=17)
res = AerSampler.from_backend(sim).run([qc], shots=1000).result()
counts = res[0].data.c.get_counts()
best = max(counts, key=counts.get)
print("ideal counts:", counts)
print(f"theta estimate = 0.{best} (binary)"
      f" = {int(best, 2) / 2 ** m}")

backend = FakeFez()                       # the same circuit, noisy
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
print("ISA ops:", dict(isa.count_ops()))
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
res = AerSampler.from_backend(sim).run([isa], shots=2000).result()
counts = res[0].data.c.get_counts()
for bits, n in sorted(counts.items(), key=lambda kv: -kv[1])[:4]:
    print(f"noisy {bits}  {n:5d}  ({n / 2000:.3f})")
