# The same circuit on the ideal and on the noisy simulator.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

qc = QuantumCircuit(3)
qc.x([0, 1, 2])          # ideal answer: always 111
qc.measure_all()

shots = 2000
ideal = StatevectorSampler(seed=1).run([qc], shots=shots).result()
ideal_counts = ideal[0].data.meas.get_counts()

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
noisy = AerSampler.from_backend(sim).run([isa], shots=shots).result()
noisy_counts = noisy[0].data.meas.get_counts()

print("ideal:", dict(sorted(ideal_counts.items())))
print("noisy:", dict(sorted(noisy_counts.items())))
good = noisy_counts.get("111", 0) / shots
print(f"noisy success rate: {good:.3f}")
