# norun
"""Ask IBM's Estimator to mitigate errors (needs an account)."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_estimator import Estimator

service = QiskitRuntimeService()          # uses your saved account
backend = service.least_busy(operational=True, simulator=False)

ghz = QuantumCircuit(4)                # no measurements: Estimator
ghz.h(0)
for q in range(3):
    ghz.cx(q, q + 1)
obs = SparsePauliOp(["ZZII", "IZZI", "IIZZ"])  # neighbour pairs

pm = generate_preset_pass_manager(optimization_level=2,
                                  backend=backend)
isa = pm.run(ghz)
pub = (isa, obs.apply_layout(isa.layout))

for level in [0, 1, 2]:
    est = Estimator(mode=backend)
    est.options.resilience_level = level  # 0 none, 1 TREX, 2 +ZNE
    est.options.default_precision = 0.02
    if level == 2:                        # fine-tune the ZNE step
        est.options.resilience.zne.noise_factors = (1, 3, 5)
        est.options.resilience.zne.extrapolator = "exponential"
    est.options.dynamical_decoupling.enable = True
    job = est.run([pub])
    print(level, job.job_id(), job.result()[0].data.evs)
