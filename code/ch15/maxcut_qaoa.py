"""Reusable MaxCut pieces: graph, cost Hamiltonian, QAOA circuit."""
from collections import Counter
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp

EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (0, 4)]
N = 5

def cost_hamiltonian():
    # H_C = sum over edges of (Z_i Z_j - 1)/2, so <z|H_C|z> = -cut(z)
    terms = [("ZZ", [i, j], 0.5) for i, j in EDGES]
    terms.append(("", [], -0.5 * len(EDGES)))
    return SparsePauliOp.from_sparse_list(terms, num_qubits=N)

def qaoa_circuit(p):
    gamma = ParameterVector("g", p)
    beta = ParameterVector("b", p)
    qc = QuantumCircuit(N)
    qc.h(range(N))                     # uniform superposition
    for layer in range(p):
        for i, j in EDGES:             # cost layer exp(-i g H_C)
            qc.rzz(gamma[layer], i, j)
        qc.rx(2 * beta[layer], range(N))   # mixer exp(-i b sum X)
    return qc

if __name__ == "__main__":
    # Brute force: the diagonal of H_C lists -cut for all 32 strings
    diag = cost_hamiltonian().to_matrix(sparse=True).diagonal().real
    cuts = {format(k, "05b"): int(-d) for k, d in enumerate(diag)}
    best = max(cuts.values())
    print(f"maximum cut: {best} of {len(EDGES)} edges")
    print("optimal strings (q4...q0):",
          [s for s, c in cuts.items() if c == best])
    print("strings per cut value:",
          dict(sorted(Counter(cuts.values()).items())))
    print("average cut of a random string:",
          sum(cuts.values()) / 32)
    qc = qaoa_circuit(1)
    print("parameter order:", [prm.name for prm in qc.parameters])
