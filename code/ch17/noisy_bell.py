"""A hand-built noise model applied to a Bell-pair circuit."""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (NoiseModel, ReadoutError,
                              depolarizing_error)
from qiskit_aer.primitives import SamplerV2 as AerSampler

noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(0.002, 1),
                                  ["h"])
noise.add_all_qubit_quantum_error(depolarizing_error(0.04, 2),
                                  ["cx"])
# Row k: probabilities of reading 0 and 1 when the truth is k
noise.add_all_qubit_readout_error(ReadoutError([[0.98, 0.02],
                                                [0.05, 0.95]]))
print("instructions with noise:", sorted(noise.noise_instructions))

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

for label, model in [("ideal", None), ("noisy", noise)]:
    sim = AerSimulator(noise_model=model, seed_simulator=2024)
    sampler = AerSampler.from_backend(sim)
    counts = sampler.run([qc], shots=4000).result()[0].data.meas
    counts = dict(sorted(counts.get_counts().items()))
    bad = (counts.get("01", 0) + counts.get("10", 0)) / 4000
    print(f"{label}: {counts}   P(01 or 10) = {bad:.4f}")
