# Measuring in the Bell basis: undo the Bell circuit, then measure
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def bell(z_bit, x_bit):
    qc = QuantumCircuit(2)
    if x_bit:
        qc.x(1)
    qc.h(0)
    if z_bit:
        qc.z(0)
    qc.cx(0, 1)
    return qc

sampler = StatevectorSampler(seed=5)
names = {(0, 0): "Phi+", (1, 0): "Phi-",
         (0, 1): "Psi+", (1, 1): "Psi-"}
for (z, x), name in names.items():
    qc = bell(z, x)
    qc.cx(0, 1)                  # reverse the entangling step
    qc.h(0)                      # and the Hadamard
    qc.measure_all()
    res = sampler.run([qc], shots=500).result()[0]
    counts = res.data.meas.get_counts()
    print(f"prepared {name:5s} -> measured {counts}")
