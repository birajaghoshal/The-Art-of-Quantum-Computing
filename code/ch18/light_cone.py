"""Which qubits can influence <Z_50> in a 100-spin chain?"""
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.converters import circuit_to_dag
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter

N, dt = 100, 0.25
bonds = list(range(0, N - 1, 2)) + list(range(1, N - 1, 2))
H = SparsePauliOp.from_sparse_list(
    [("ZZ", [i, i + 1], -1.0) for i in bonds] +
    [("X", [i], -0.6) for i in range(N)], num_qubits=N)

for k in [1, 2, 4, 8, 16, 32]:
    qc = QuantumCircuit(N)
    gate = PauliEvolutionGate(H, time=k * dt,
                              synthesis=LieTrotter(reps=k))
    qc.append(gate, range(N))
    dag = circuit_to_dag(qc.decompose())
    cone = dag.quantum_causal_cone(qc.qubits[50])  # back from Z_50
    two_q = dag.count_ops().get("rzz", 0)
    print(f"{k:2d} steps: light cone {len(cone):3d} of {N} qubits, "
          f"full circuit {two_q:4d} RZZ gates")
