import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector

def qpe(phi, t):
    """Phase estimation for P(phi) with t counting qubits."""
    qc = QuantumCircuit(t + 1)
    qc.x(t)                               # eigenstate |1>
    qc.h(range(t))
    for k in range(t):                    # controlled-P(phi)^(2^k)
        qc.cp(2 ** k * phi, k, t)         # = controlled-P(2^k phi)
    qc.append(QFTGate(t).inverse(), range(t))
    return qc

t, phi = 4, 2 * np.pi * 11 / 16
qc = QuantumCircuit(t + 1, t)
qc.compose(qpe(phi, t), inplace=True)
qc.measure(range(t), range(t))            # counting register only
res = StatevectorSampler(seed=4).run([qc], shots=1000).result()
print("phi = 2 pi * 11/16, counts:", res[0].data.c.get_counts())

print("theta     t   outcome  estimate  P(outcome)")
for theta, t in [(3 / 8, 3), (11 / 16, 4), (0.71875, 5)]:
    probs = Statevector(qpe(2 * np.pi * theta, t)).probabilities(
        qargs=list(range(t)))
    m = int(np.argmax(probs))
    print(f"{theta:<8}  {t}   {m:0{t}b}"
          f"{' ' * (8 - t)} {m / 2 ** t:<8}  {probs[m]:.3f}")
