from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
print(" n   H   cp  swap | FakeFez: cz  depth")
for n in range(2, 9):
    hs, cps, swaps = n, n * (n - 1) // 2, n // 2
    qc = QuantumCircuit(n)
    qc.append(QFTGate(n), range(n))
    isa = pm.run(qc)
    cz = isa.count_ops().get('cz', 0)
    print(f"{n:2d}  {hs:2d}  {cps:3d}  {swaps:4d} |"
          f"       {cz:4d}  {isa.depth():5d}")
