# norun
"""Capstone on a real QPU: Estimator with built-in mitigation."""
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Batch
from qiskit_ibm_runtime.executor_estimator import Estimator
from tfim_model import steps, times, mag, trotter
from choose_qubits import rank_lines

service = QiskitRuntimeService()
backend = service.least_busy(       # rank_lines needs CZ gates
    operational=True, simulator=False, min_num_qubits=6,
    filters=lambda b: "cz" in b.operation_names)
best = list(rank_lines(backend)[0][0])  # today's best 6-qubit line
pm = generate_preset_pass_manager(2, backend, initial_layout=best,
                                  seed_transpiler=11)
pubs = []
for k in range(1, steps + 1):    # no measurements for Estimator
    isa = pm.run(trotter(k))
    pubs.append((isa, mag.apply_layout(isa.layout)))

with Batch(backend=backend) as batch:
    est = Estimator(mode=batch)
    est.options.default_precision = 0.01
    est.options.resilience_level = 2  # readout + ZNE, twirling on
    est.options.dynamical_decoupling.enable = True
    job = est.run(pubs)
    print("job id:", job.job_id())
    result = job.result()

for t, pub_result in zip(times[1:], result):
    ev, sd = float(pub_result.data.evs), float(pub_result.data.stds)
    print(f"t = {t:.2f}:  <m_z> = {ev:+.4f} +/- {sd:.4f}")
print("QPU seconds used:", job.usage())
