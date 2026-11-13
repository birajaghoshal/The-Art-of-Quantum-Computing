# Parameterised circuits: transpile once, bind many values
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

theta, phi = Parameter("theta"), Parameter("phi")
qc = QuantumCircuit(2)
qc.ry(theta, 0)
qc.rz(phi, 0)
qc.cx(0, 1)
print("Parameter order:", [p.name for p in qc.parameters])

bound = qc.assign_parameters({theta: np.pi / 2, phi: 0.0})
print("Parameters left after binding:", bound.num_parameters)

pm = generate_preset_pass_manager(
    optimization_level=1, backend=FakeFez(), seed_transpiler=11)
isa = pm.run(qc)                   # compiled with symbols intact
print("ISA circuit still has:", [p.name for p in isa.parameters])

values = np.array([[0, 0], [np.pi / 2, 0], [np.pi / 2, np.pi / 3],
                   [np.pi / 2, np.pi / 2], [np.pi, 0]])
obs = SparsePauliOp("XX").apply_layout(isa.layout)
est = AerEstimator()                # ideal, runs ISA circuits
evs = est.run([(isa, obs, {(theta, phi): values})]
              ).result()[0].data.evs
for (t, p), e in zip(values, evs):
    ev = round(e, 3) + 0               # + 0 avoids printing -0.000
    print(f"theta = {t:.3f}, phi = {p:.3f}  ->  <XX> = {ev:+.3f}")
