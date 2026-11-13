# One circuit at optimization levels 0-3 on FakeFez
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(6)
qc.append(QFTGate(6), range(6))   # every qubit talks to every other
qc.measure_all()

backend = FakeFez()
print("level  depth  2q-depth   cz  1q-gates  total")
for level in range(4):
    pm = generate_preset_pass_manager(optimization_level=level,
                                      backend=backend,
                                      seed_transpiler=11)
    isa = pm.run(qc)
    ops = isa.count_ops()
    one_q = sum(ops.get(g, 0) for g in ("rz", "sx", "x"))
    d2 = isa.depth(lambda inst: inst.operation.num_qubits == 2)
    print(f"{level:5d}  {isa.depth():5d}  {d2:8d}  {ops['cz']:3d}"
          f"  {one_q:8d}  {isa.size():5d}")
