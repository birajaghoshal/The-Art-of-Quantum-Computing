# norun
# Running the feed-forward circuit on a real IBM Quantum device
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler

q, c = QuantumRegister(2, "q"), ClassicalRegister(2, "c")
qc = QuantumCircuit(q, c)
qc.h(0)
qc.cx(0, 1)
qc.measure(0, c[0])
with qc.if_test((c[0], 1)):
    qc.x(1)
qc.measure(1, c[1])

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
job = Sampler(mode=backend).run([isa], shots=4000)
print("Job ID:", job.job_id())
counts = job.result()[0].data.c.get_counts()
print("Counts (c1 c0):", dict(sorted(counts.items())))
