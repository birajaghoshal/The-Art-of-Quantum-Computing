"""Count the neighbours of every qubit in the coupling map.
The map itself is drawn by fig_gatemap.py."""
from collections import Counter
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
cmap = backend.coupling_map
degree = [len(cmap.neighbors(q)) for q in range(backend.num_qubits)]
for d, k in sorted(Counter(degree).items()):
    print(f"qubits with {d} neighbour(s): {k}")
print("average degree:", round(sum(degree) / len(degree), 3))
