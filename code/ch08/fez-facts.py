# What does the FakeFez backend accept?
from collections import Counter
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
target = backend.target
print("Qubits:", backend.num_qubits)
ops = sorted(backend.operation_names)
print("Operations:", ", ".join(ops[:6]))
print("           ", ", ".join(ops[6:]))

cmap = backend.coupling_map
print("Connected pairs:", len(cmap.get_edges()) // 2)
degree = Counter(len(cmap.neighbors(q)) for q in range(156))
print("Qubits with 1, 2, 3 neighbours:",
      [degree[k] for k in (1, 2, 3)])
print("Neighbours of qubit 3:", sorted(cmap.neighbors(3)))
print("Shortest path 0 -> 20:", cmap.shortest_undirected_path(0, 20))

print(f"CZ error on (3, 4): {target['cz'][(3, 4)].error:.4f}")
print(f"SX error on 3:      {target['sx'][(3,)].error:.5f}")
print(f"Readout error on 3: {target['measure'][(3,)].error:.4f}")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
for inst in qc.data:
    name = inst.operation.name
    print(f"Is '{name}' native?", name in target.operation_names)
