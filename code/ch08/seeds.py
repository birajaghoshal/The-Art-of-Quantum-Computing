# Routing is randomised: compare ten seeds at levels 1 and 3
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(6)
qc.append(QFTGate(6), range(6))
backend = FakeFez()
for level in (1, 3):
    counts = []
    for seed in range(10):
        pm = generate_preset_pass_manager(optimization_level=level,
                                          backend=backend,
                                          seed_transpiler=seed)
        counts.append(pm.run(qc).count_ops()["cz"])
    best = counts.index(min(counts))
    print(f"level {level}: cz counts {counts}")
    print(f"         min {min(counts)} (seed {best}), "
          f"max {max(counts)}, mean {sum(counts) / 10:.1f}")
