# Build all four Bell states from |00> with optional X and Z
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.primitives import StatevectorSampler

def bell(z_bit, x_bit):
    qc = QuantumCircuit(2)
    if x_bit:
        qc.x(1)                  # prepare |1> on the target first
    qc.h(0)
    if z_bit:
        qc.z(0)                  # sign flip on the control branch
    qc.cx(0, 1)
    return qc

names = {(0, 0): "Phi+", (1, 0): "Phi-",
         (0, 1): "Psi+", (1, 1): "Psi-"}
circuits = []
for (z, x), name in names.items():
    qc = bell(z, x)
    amps = {str(k): round(float(v.real), 3)
            for k, v in Statevector(qc).to_dict().items()}
    print(f"{name:5s} amplitudes {amps}")
    qc.measure_all()
    circuits.append(qc)

sampler = StatevectorSampler(seed=np.random.default_rng(21))
results = sampler.run(circuits, shots=1000).result()
for name, res in zip(names.values(), results):
    counts = dict(sorted(res.data.meas.get_counts().items()))
    print(f"{name:5s} counts {counts}")
