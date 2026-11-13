# norun
"""Evaluate the H2 energy at the VQE optimum on an IBM QPU."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_estimator import Estimator

H = SparsePauliOp.from_list([
    ("II", -1.052373), ("IZ", 0.397937), ("ZI", -0.397937),
    ("ZZ", -0.011280), ("XX", 0.180931)])
qc = QuantumCircuit(2)
qc.ry(-0.2235, 0)
qc.cx(0, 1)
qc.x(0)

service = QiskitRuntimeService()        # uses your saved account
backend = service.least_busy(operational=True, simulator=False)
pm = generate_preset_pass_manager(optimization_level=1,
                                  backend=backend)
isa = pm.run(qc)
estimator = Estimator(mode=backend)
# 10 mHa standard error: an order-of-magnitude check,
# not chemical accuracy
job = estimator.run([(isa, H.apply_layout(isa.layout))],
                    precision=0.01)
print("backend:", backend.name, " job id:", job.job_id())
ev = float(job.result()[0].data.evs)
print(f"total energy: {ev + 0.719969:.4f} Ha (exact -1.1373)")
