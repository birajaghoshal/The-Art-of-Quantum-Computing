# norun
"""Job mode: one self-contained request to a real QPU."""
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler

service = QiskitRuntimeService()    # reads your saved credentials
backend = service.least_busy(operational=True, simulator=False,
                             min_num_qubits=6)
print("running on", backend.name)

qc = QuantumCircuit(6)              # step 1: map the problem
qc.h(0)
for q in range(5):
    qc.cx(q, q + 1)
qc.measure_all()

pm = generate_preset_pass_manager(optimization_level=2,
                                  backend=backend)
isa = pm.run(qc)                    # step 2: optimise for the QPU

sampler = Sampler(mode=backend)     # step 3: execute (job mode)
job = sampler.run([isa], shots=4000)
print("job id:", job.job_id())      # keep this for your notes

result = job.result()               # waits in the queue, then runs
counts = result[0].data.meas.get_counts()
good = counts.get("000000", 0) + counts.get("111111", 0)  # step 4
print(f"GHZ success fraction: {good / sum(counts.values()):.3f}")
print("QPU usage (s):", job.usage())
