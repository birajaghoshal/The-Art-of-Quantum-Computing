"""BB84 with an optional intercept-resend eavesdropper."""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

def run_bb84(n, eve=0.0, seed=1):
    """Send n qubits; Eve intercepts each with probability eve.
    Basis 0 means Z (|0>, |1>), basis 1 means X (|+>, |->)."""
    rng = np.random.default_rng(seed)
    a_bit, a_basis, b_basis, e_basis = rng.integers(0, 2, (4, n))
    tapped = rng.random(n) < eve
    e_reg = ClassicalRegister(n, "e")
    b_reg = ClassicalRegister(n, "b")
    qc = QuantumCircuit(QuantumRegister(n), e_reg, b_reg)
    for i in range(n):                 # one qubit per transmission
        if a_bit[i]:
            qc.x(i)
        if a_basis[i]:
            qc.h(i)
        if tapped[i]:                  # Eve measures, then resends
            if e_basis[i]:
                qc.h(i)
            qc.measure(i, e_reg[i])
            if e_basis[i]:
                qc.h(i)
        if b_basis[i]:
            qc.h(i)
        qc.measure(i, b_reg[i])
    sim = AerSimulator(method="stabilizer", seed_simulator=seed)
    data = AerSampler.from_backend(sim).run([qc], shots=1)\
        .result()[0].data
    bits = lambda reg: np.array([int(c) for c in
                                 reg.get_bitstrings()[0][::-1]])
    return dict(a_bit=a_bit, a_basis=a_basis, b_basis=b_basis,
                b_bit=bits(data.b), e_bit=bits(data.e),
                e_basis=e_basis, tapped=tapped)
