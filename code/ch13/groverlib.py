# Grover building blocks made by hand from H, X and MCX gates
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

def mcz(qc, qubits):
    """Multi-controlled Z: H on the last qubit turns MCX into MCZ."""
    *controls, target = qubits
    qc.h(target)
    qc.append(MCXGate(len(controls)), [*controls, target])
    qc.h(target)

def phase_oracle(n, marked):
    """Flip the sign of each bitstring in `marked` (Qiskit order)."""
    qc = QuantumCircuit(n, name="oracle")
    for s in marked:
        zeros = [i for i, b in enumerate(reversed(s)) if b == "0"]
        if zeros:
            qc.x(zeros)              # map |s> to |11...1>
        mcz(qc, list(range(n)))      # flip the sign of |11...1>
        if zeros:
            qc.x(zeros)              # map back
    return qc

def diffuser(n):
    """Reflection about the uniform state |s> (up to a global -1)."""
    qc = QuantumCircuit(n, name="diffuser")
    qc.h(range(n))
    qc.x(range(n))
    mcz(qc, list(range(n)))          # flips the sign of |00...0>
    qc.x(range(n))
    qc.h(range(n))
    return qc

def grover_circuit(n, marked, k, measure=True):
    """Uniform superposition followed by k Grover iterations."""
    qc = QuantumCircuit(n)
    qc.h(range(n))
    oracle, diff = phase_oracle(n, marked), diffuser(n)
    for _ in range(k):
        qc.compose(oracle, inplace=True)
        qc.compose(diff, inplace=True)
    if measure:
        qc.measure_all()
    return qc

def theory(N, M, k):
    """Exact success probability after k iterations."""
    half_theta = np.arcsin(np.sqrt(M / N))
    return np.sin((2 * k + 1) * half_theta) ** 2

def best_k(N, M):
    """Iteration count that maximises the success probability."""
    return int(np.floor(np.pi / (4 * np.arcsin(np.sqrt(M / N)))))

if __name__ == "__main__":
    for N, M in [(4, 1), (8, 1), (16, 1), (16, 3), (1024, 1)]:
        k = best_k(N, M)
        print(f"N = {N:>4}, M = {M}: best k = {k:>2}, "
              f"P(success) = {theory(N, M, k):.4f}")
