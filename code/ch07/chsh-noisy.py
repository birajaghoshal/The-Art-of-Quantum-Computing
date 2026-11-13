# The same CHSH test on a noisy simulator modelled on IBM Fez
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_ibm_runtime.fake_provider import FakeFez

def obs(label_a, angle):
    return SparsePauliOp.from_sparse_list(
        [(label_a + "Z", [0, 1], np.cos(angle)),
         (label_a + "X", [0, 1], np.sin(angle))], 2)

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
t = np.pi / 4
ops = [obs("Z", t), obs("Z", -t), obs("X", t), obs("X", -t)]

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
isa_ops = [o.apply_layout(isa.layout) for o in ops]
print("Physical qubits used:", isa.layout.final_index_layout())

sim = AerSimulator.from_backend(backend, seed_simulator=1234)
opts = {"run_options": {"seed_simulator": 1234}}  # seeds shot noise
est = AerEstimator.from_backend(sim, options=opts)
res = est.run([(isa, isa_ops)], precision=0.01).result()[0]
E = res.data.evs
print("Correlators:", E.round(4))
S = E[0] + E[1] + E[2] - E[3]
print(f"noisy S = {S:.4f}"
      f"  (ideal {2 * np.sqrt(2):.4f}, classical 2)")
print(f"standard error per correlator = {res.data.stds[0]:.3f}")
