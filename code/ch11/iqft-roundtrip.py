import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.primitives import StatevectorSampler

n, j = 3, 4                               # hide the integer 4 = 100

def fourier_state(j, reverse=False):
    """Prepare QFT|j> from the product formula (optionally with
    the qubit order reversed, as a swap-free QFT would leave it)."""
    qc = QuantumCircuit(n)
    for l in range(n):
        q = n - 1 - l if reverse else l
        qc.h(q)
        qc.p(2 * np.pi * j / 2 ** (n - l), q)
    return qc

def qft_no_swaps(n):
    qc = QuantumCircuit(n)
    for t in reversed(range(n)):
        qc.h(t)
        for c in reversed(range(t)):
            qc.cp(np.pi / 2 ** (t - c), c, t)
    return qc

undo = QuantumCircuit(n)
undo.append(QFTGate(n).inverse(), range(n))
cases = {"QFTGate inverse     ": fourier_state(j).compose(undo),
         "no swaps, reversed  ": fourier_state(j, True).compose(
             qft_no_swaps(n).inverse()),
         "no swaps, mismatched": fourier_state(j).compose(
             qft_no_swaps(n).inverse())}
sampler = StatevectorSampler(seed=8)
for label, qc in cases.items():
    qc.measure_all()
    counts = sampler.run([qc], shots=200).result()[0].data.meas
    print(label, dict(sorted(counts.get_counts().items())))
