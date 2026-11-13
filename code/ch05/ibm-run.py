# norun
# The three-coin circuit on a real IBM quantum computer.
from math import pi
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler

qc = QuantumCircuit(3)
qc.h(0)
qc.x(1)
qc.ry(2 * pi / 3, 2)
qc.measure_all()

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print("running on", backend.name)

pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)                          # ISA circuit for this QPU

sampler = Sampler(mode=backend)           # job mode
job = sampler.run([isa], shots=1000)      # 1000 shots: a few seconds
print("job id:", job.job_id())            # write this down!
counts = job.result()[0].data.meas.get_counts()
print(dict(sorted(counts.items())))
