# Play CHSH with measurement outcomes on the noisy Fez model
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

def round_circuit(x, y):  # one setting pair (x for Alice, y Bob)
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    if x == 1:
        qc.h(0)                  # Alice measures X instead of Z
    qc.ry(-np.pi / 4 if y == 0 else np.pi / 4, 1)  # Bob's direction
    qc.measure_all()
    return qc

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
settings = [(0, 0), (0, 1), (1, 0), (1, 1)]
isa = [pm.run(round_circuit(x, y)) for x, y in settings]
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
results = AerSampler.from_backend(sim).run(isa, shots=4000).result()

S, wins = 0.0, 0.0
for (x, y), res in zip(settings, results):
    c = res.data.meas.get_counts()
    same = c.get("00", 0) + c.get("11", 0)
    E = (2 * same - 4000) / 4000         # P(same) - P(different)
    S += -E if (x, y) == (1, 1) else E
    wins += (4000 - same if x * y else same) / 4000 / 4
    print(f"x={x} y={y}  E = {E:+.4f}")
print(f"S = {S:.4f},  win rate = {wins:.4f}")
