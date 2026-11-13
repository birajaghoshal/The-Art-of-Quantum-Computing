"""H2 energy at the VQE optimum: ideal versus the FakeFez model."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import (StatevectorEstimator,
                               StatevectorSampler)
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

H = SparsePauliOp.from_list([
    ("II", -1.052373), ("IZ", 0.397937), ("ZI", -0.397937),
    ("ZZ", -0.011280), ("XX", 0.180931)])
E_nuc, exact = 0.719969, -1.137305
qc = QuantumCircuit(2)       # one-parameter ansatz at its optimum
qc.ry(-0.2235, 0)
qc.cx(0, 1)
qc.x(0)

backend = FakeFez()
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
def energy_from_counts(r):          # r: results of [zc, xc]
    cz, cx = (r[k].data.meas.get_counts() for k in (0, 1))
    total = 0.0
    for label, c in H.to_list():
        counts = cx if "X" in label else cz
        qubits = [q for q in range(2) if label[-1 - q] != "I"]
        # average of (-1)^(sum of the measured bits on those qubits)
        avg = sum(n * (-1) ** sum(int(s[-1 - q]) for q in qubits)
                  for s, n in counts.items()) / sum(counts.values())
        total += c.real * avg
    return total

zc = qc.copy()
zc.measure_all()                    # setting 1: II, IZ, ZI, ZZ
xc = qc.copy()
xc.h([0, 1])                        # setting 2: rotate X into Z
xc.measure_all()
e = {"ideal estimator": StatevectorEstimator().run([(qc, H)])
     .result()[0].data.evs}
sv_sampler = StatevectorSampler(seed=np.random.default_rng(7))
r = sv_sampler.run([zc, xc], shots=4000).result()
e["ideal sampler, 4000 shots"] = energy_from_counts(r)
isa = pm.run(qc)
opts = {"run_options": {"seed_simulator": 1234}}   # reproducible
aer_est = AerEstimator.from_backend(sim, options=opts)
e["noisy Aer estimator"] = aer_est.run(
    [(isa, H.apply_layout(isa.layout))]).result()[0].data.evs
r = AerSampler.from_backend(sim).run(pm.run([zc, xc]),
                                     shots=4000).result()
e["noisy sampler, 4000 shots"] = energy_from_counts(r)
for name, val in e.items():
    tot = float(val) + E_nuc
    err = round(1000 * (tot - exact), 1) + 0.0     # avoid "-0.0"
    print(f"{name:26s} E = {tot:.4f} Ha, error = {err:5.1f} mHa")
