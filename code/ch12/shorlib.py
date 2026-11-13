# Helpers for order finding with a truth-table modular multiplier
from fractions import Fraction
from math import gcd
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFTGate, UnitaryGate

def modmul_gate(a, N, n):
    """Permutation gate |y> -> |a*y mod N> (y >= N kept)."""
    U = np.zeros((2**n, 2**n))
    for y in range(2**n):
        U[(a * y) % N if y < N else y, y] = 1
    return UnitaryGate(U, label=f"x{a} mod {N}")

def order_finding(a, N, t):
    """Phase estimation of U_a with t counting qubits."""
    n = N.bit_length()
    count = QuantumRegister(t, "count")
    work = QuantumRegister(n, "work")
    qc = QuantumCircuit(count, work, ClassicalRegister(t, "c"))
    qc.h(count)
    qc.x(work[0])                       # work register starts in |1>
    for j in range(t):
        a_j = pow(a, 2**j, N)   # U^(2^j) multiplies by a^(2^j)
        cu = modmul_gate(a_j, N, n).control(1)
        qc.append(cu, [count[j], *work])
    qc.append(QFTGate(t).inverse(), count)
    qc.measure(count, range(t))
    return qc

def guess_order(k, t, a, N, max_mult=1):
    """Measured k -> order r (or None) via continued fractions.
    If max_mult > 1, also try small multiples of the denominator."""
    r = Fraction(k, 2**t).limit_denominator(N).denominator
    for m in range(1, max_mult + 1):
        if pow(a, m * r, N) == 1:
            return m * r
    return None

def factors_from_order(a, r, N):
    """Classical last step: split N using a^(r/2), or None."""
    if r is None or r % 2 == 1:
        return None
    half = pow(a, r // 2, N)
    if half == N - 1:
        return None
    p = gcd(half - 1, N)
    return (p, N // p) if 1 < p < N else None

if __name__ == "__main__":
    qc = order_finding(7, 15, 8)
    print("qubits:", qc.num_qubits, " ops:", dict(qc.count_ops()))
    print("guess_order(192, 8, 7, 15) =", guess_order(192, 8, 7, 15))
    print("factors_from_order(7, 4, 15) =",
          factors_from_order(7, 4, 15))
