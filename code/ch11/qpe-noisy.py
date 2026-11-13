import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
sampler = AerSampler.from_backend(
    AerSimulator.from_backend(backend, seed_simulator=1234))

print(" t  ideal answer  cz gates  depth  P(answer), noisy")
for t in (3, 4, 5, 6):
    qc = QuantumCircuit(t + 1, t)
    qc.x(t)
    qc.h(range(t))
    for k in range(t):
        qc.cp(2 ** k * np.pi / 4, k, t)       # T = P(pi/4)
    qc.append(QFTGate(t).inverse(), range(t))
    qc.measure(range(t), range(t))
    answer = format(2 ** (t - 3), f"0{t}b")      # theta = 1/8
    isa = pm.run(qc)
    counts = sampler.run([isa], shots=2000).result()[0].data.c
    p = counts.get_counts().get(answer, 0) / 2000
    print(f"{t:2d}  {answer:<12}  {isa.count_ops().get('cz', 0):8d}"
          f"  {isa.depth():5d}  {p:.3f}")
