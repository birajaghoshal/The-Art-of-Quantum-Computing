# norun
"""Session mode: an iterative loop that keeps its place on the QPU."""
import numpy as np
from scipy.optimize import minimize
from qiskit.circuit.library import real_amplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Session
from qiskit_ibm_runtime.executor_estimator import Estimator

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
# imports, service and backend as in job_mode.py (see full file)
ham = SparsePauliOp(["ZZ", "XI", "IX"], coeffs=[1.0, 0.6, 0.6])
ansatz = real_amplitudes(2, reps=2)
isa = generate_preset_pass_manager(optimization_level=2,
                                   backend=backend).run(ansatz)
isa_ham = ham.apply_layout(isa.layout)

# max_time caps how long the session may stay open
with Session(backend=backend, max_time="10m") as session:
    est = Estimator(mode=session)
    est.options.default_precision = 0.02
    est.options.resilience_level = 1

    def energy(x):                      # every call is a quick job
        return est.run([(isa, isa_ham, x)]).result()[0].data.evs

    x0 = np.zeros(ansatz.num_parameters)
    out = minimize(energy, x0, method="COBYLA",
                   options={"maxiter": 30})
print("lowest energy found:", round(float(out.fun), 3))
