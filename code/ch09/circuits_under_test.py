"""Circuits under test. CH09_MUTANT switches inject known bugs."""
import os
from qiskit import QuantumCircuit

def mutant():
    return os.environ.get("CH09_MUTANT", "")

def encode_bits(bits):
    """Basis state |bits>, with bits written "q_{n-1} ... q_0"."""
    qc = QuantumCircuit(len(bits))
    order = bits if mutant() == "reversed bits" else bits[::-1]
    for q, b in enumerate(order):
        if b == "1":
            qc.x(q)
    return qc

def swap_from_cx():
    qc = QuantumCircuit(2)
    qc.cx(0, 1); qc.cx(1, 0)
    if mutant() != "missing cx":
        qc.cx(0, 1)
    return qc

def ghz(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    for q in range(n - 1):
        qc.cx(q, q + 1)
    if mutant() == "phase flip":
        qc.z(0)
    return qc
