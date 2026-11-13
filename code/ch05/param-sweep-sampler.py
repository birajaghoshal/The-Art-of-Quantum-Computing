# One parameterised circuit, many angles, one Sampler call.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorSampler

theta = Parameter("θ")
qc = QuantumCircuit(1)
qc.ry(theta, 0)
qc.measure_all()
print("parameters:", qc.parameters)

angles = np.linspace(0, np.pi, 5)          # 5 values of theta
rng = np.random.default_rng(5)     # fresh draws for every angle
sampler = StatevectorSampler(seed=rng)
pub = (qc, angles)                          # bind by position in PUB
data = sampler.run([pub], shots=400).result()[0].data.meas
print("result shape:", data.shape, " shots each:", data.num_shots)

for i, t in enumerate(angles):
    ones = data.get_counts(i).get("1", 0)
    theory = np.sin(t / 2) ** 2
    print(f"θ = {t:.3f}  P(1) measured {ones / 400:.3f}"
          f"  theory {theory:.3f}")
