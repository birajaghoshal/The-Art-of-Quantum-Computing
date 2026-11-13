"""Transverse-field Ising chain: Hamiltonian, exact and Trotter."""
import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.synthesis import LieTrotter

n, J, h, dt, steps = 6, 1.0, 0.6, 0.25, 10
bonds = [0, 2, 4, 1, 3]                  # even bonds, then odd bonds
zz = [("ZZ", [i, i + 1], -J) for i in bonds]
xs = [("X", [i], -h) for i in range(n)]
H = SparsePauliOp.from_sparse_list(zz + xs, num_qubits=n)
mag = SparsePauliOp.from_sparse_list(          # m_z = mean of Z_i
    [("Z", [i], 1 / n) for i in range(n)], num_qubits=n)
times = dt * np.arange(steps + 1)

def trotter(k, fold=0, synthesis=None):
    """k Trotter steps of length dt, globally folded 'fold' times."""
    u = QuantumCircuit(n)
    if k:
        synth = synthesis or LieTrotter(reps=k)
        u.append(PauliEvolutionGate(H, time=k * dt, synthesis=synth),
                 range(n))
    u = u.decompose()                 # expose gates so we can invert
    out = u.copy()
    for _ in range(fold):
        out.barrier()
        out.compose(u.inverse(), inplace=True)
        out.barrier()
        out.compose(u, inplace=True)
    return out

def exact_state(t):
    """exp(-iHt)|000000> from the full 64 x 64 matrix exponential."""
    psi0 = np.zeros(2**n)
    psi0[0] = 1.0                     # all spins up: |000000>
    return expm(-1j * H.to_matrix() * t) @ psi0

def exact_curve(ts):
    Mm = mag.to_matrix()
    return np.array([np.vdot(v, Mm @ v).real
                     for v in map(exact_state, ts)])

if __name__ == "__main__":
    print(f"H has {len(H)} Pauli terms, e.g. {H.paulis[0]} and "
          f"{H.paulis[-1]}")
    exact = exact_curve(times)
    print(" t    exact    Trotter  RZZ gates  depth")
    for k in range(0, steps + 1, 2):
        qc = trotter(k)
        ideal = Statevector(qc).expectation_value(mag).real
        print(f"{times[k]:.2f}  {exact[k]:+.4f}  {ideal:+.4f}  "
              f"{qc.count_ops().get('rzz', 0):6d}  {qc.depth():6d}")
