"""First look at a fake IBM backend: size, gates and connections."""
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()          # offline snapshot of a 156-qubit device
target = backend.target      # everything the compiler needs to know

print("Backend name:     ", backend.name)
print("Number of qubits: ", backend.num_qubits)
ops = sorted(target.operation_names)
print("Operations:       ", ", ".join(ops[:6]))
print("                  ", ", ".join(ops[6:]))

# The unitary gates among them form the basis set
gates = [g for g in sorted(target.operation_names)
         if g in ("cz", "id", "rz", "sx", "x")]
print("Basis gates:      ", gates)

# The coupling map lists directed pairs (a, b) where cz is allowed
edges = backend.coupling_map.get_edges()
links = {tuple(sorted(e)) for e in edges}
print("Directed pairs:   ", len(edges))
print("Physical links:   ", len(links))
print("Time step dt (ns):", target.dt * 1e9)
