# norun
"""Batch mode: many independent jobs scheduled together."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Batch
from qiskit_ibm_runtime.executor_sampler import Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_fez")    # or any device you can use

theta = Parameter("theta")
qc = QuantumCircuit(2)
qc.ry(theta, 0)
qc.cx(0, 1)
qc.measure_all()
isa = generate_preset_pass_manager(optimization_level=1,
                                   backend=backend).run(qc)

angle_sets = np.split(np.linspace(0, np.pi, 40), 4)   # 4 chunks
with Batch(backend=backend) as batch:
    sampler = Sampler(mode=batch)
    jobs = [sampler.run([(isa, angles)], shots=2000)
            for angles in angle_sets]
    for job in jobs:                    # results arrive as jobs end
        bits = job.result()[0].data.meas
        print(job.job_id(), bits.num_shots, "shots per angle")
print("batch usage (s):", batch.usage())
