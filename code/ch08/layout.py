# Choosing the physical qubits yourself with initial_layout
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(4)
qc.h(0)
for k in range(3):
    qc.cx(k, k + 1)               # needs the chain 0-1-2-3
qc.measure_all()

backend = FakeFez()
layouts = {"a line [4,5,6,7]": [4, 5, 6, 7],
           "a branch [2,3,4,16]": [2, 3, 4, 16],
           "spread [0,20,40,60]": [0, 20, 40, 60]}
for name, phys in layouts.items():
    pm = generate_preset_pass_manager(optimization_level=1,
                                      backend=backend,
                                      initial_layout=phys,
                                      seed_transpiler=11)
    isa = pm.run(qc)
    final = isa.layout.final_index_layout()
    print(f"{name:20s} cz = {isa.count_ops()['cz']:2d}, "
          f"depth = {isa.depth():3d}, final = {final}")
