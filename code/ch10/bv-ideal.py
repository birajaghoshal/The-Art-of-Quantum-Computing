from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

secret = "110101"                        # written q5 q4 q3 q2 q1 q0
n = len(secret)

def bv_circuit(s):
    qc = QuantumCircuit(n + 1, n)        # qubit n is the output y
    qc.x(n)
    qc.h(range(n + 1))
    qc.barrier()
    for q, bit in enumerate(reversed(s)):   # s[-1] belongs to q0
        if bit == "1":
            qc.cx(q, n)                  # f(x) = s . x  (mod 2)
    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

qc = bv_circuit(secret)

sampler = StatevectorSampler(seed=3)
counts = sampler.run([qc], shots=1).result()[0].data.c.get_counts()
print("one shot:", counts, " secret:", secret)
