# Grover on a noisy model of a 156-qubit IBM device (FakeFez)
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez
from groverlib import grover_circuit, best_k, theory

backend = FakeFez()
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
pm = generate_preset_pass_manager(
    optimization_level=3, backend=backend, seed_transpiler=11)
sampler = AerSampler.from_backend(sim)

print(f"{'n':>2} {'k':>2} {'CZs':>5} {'depth':>6} {'ideal':>7}"
      f" {'noisy':>7} {'random guess':>13}")
for n, target in [(2, "10"), (3, "110"), (4, "1011"), (5, "10110")]:
    k = best_k(2**n, 1)
    isa = pm.run(grover_circuit(n, [target], k))
    counts = sampler.run([isa], shots=2000).result()[0].data.meas \
        .get_counts()
    noisy = counts.get(target, 0) / 2000
    print(f"{n:>2} {k:>2} {isa.count_ops().get('cz', 0):>5} "
          f"{isa.depth():>6} {theory(2**n, 1, k):>7.3f} "
          f"{noisy:>7.3f} {1 / 2**n:>13.3f}")
