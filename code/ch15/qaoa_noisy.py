"""Sample the optimised p = 2 QAOA circuit on the FakeFez model."""
from qiskit.primitives import StatevectorSampler
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez
from maxcut_qaoa import EDGES, N, qaoa_circuit

cut = lambda s: sum(s[N - 1 - i] != s[N - 1 - j] for i, j in EDGES)
qc = qaoa_circuit(2).assign_parameters([1.054, 1.214, 0.590, 0.916])
qc.measure_all()

backend = FakeFez()
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
ops = isa.count_ops()
print(f"after transpiling: depth {isa.depth()}, "
      f"CZ gates {ops.get('cz', 0)}")

runs = {"ideal": StatevectorSampler(seed=42).run([qc], shots=2000),
        "FakeFez": AerSampler.from_backend(sim).run([isa],
                                                    shots=2000)}
for name, job in runs.items():
    counts = job.result()[0].data.meas.get_counts()
    mean = sum(c * cut(s) for s, c in counts.items()) / 2000
    best = sum(c for s, c in counts.items() if cut(s) == 6) / 2000
    print(f"{name:8s} mean cut = {mean:.3f}, "
          f"P(cut = 6) = {best:.3f}")
