# Transpile a Bell circuit for FakeFez and look at the result
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)

print("Before:", dict(qc.count_ops()))
print("After: ", dict(isa.count_ops()))
print("Width before/after:", qc.num_qubits, "/", isa.num_qubits)
print("Virtual -> physical:", isa.layout.initial_index_layout()[:2])

fig = isa.draw("mpl", idle_wires=False, fold=-1, scale=0.8)
fig.savefig("figures/ch08/bell_isa.pdf", bbox_inches="tight")
