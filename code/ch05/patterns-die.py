# Qiskit patterns end to end: a fair six-sided die from qubits.
from collections import Counter
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

# 1. Map: three fair coins give 8 equally likely outcomes 0..7.
qc = QuantumCircuit(3)
qc.h([0, 1, 2])
qc.measure_all()

# 2. Optimise: rewrite for the device's gates and qubits.
backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
print("ISA operations:", dict(isa.count_ops()))

# 3. Execute: a noisy local model of the device.
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
sampler = AerSampler.from_backend(sim)
bits = sampler.run([isa], shots=3000).result()[0].data.meas

# 4. Post-process: keep outcomes 0..5 as faces 1..6, reject 6, 7.
rolls = [int(b, 2) + 1 for b in bits.get_bitstrings()
         if int(b, 2) < 6]
faces = Counter(rolls)
print("accepted rolls:", len(rolls), "of", bits.num_shots)
for face in range(1, 7):
    print(f"  face {face}: {faces[face]:4d}"
          f"  ({faces[face] / len(rolls):.3f})")
