# What the transpiler does to one Hadamard gate.
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)

print("before:", dict(qc.count_ops()))
print("after: ", dict(isa.count_ops()))
print("width of ISA circuit:", isa.num_qubits, "qubits")
phys = isa.layout.final_index_layout()
print("virtual qubit 0 placed on physical qubit", phys[0])
for inst in isa.data:
    if inst.operation.name in ("rz", "sx"):
        params = [round(float(p), 4) for p in inst.operation.params]
        print(" ", inst.operation.name, params)
