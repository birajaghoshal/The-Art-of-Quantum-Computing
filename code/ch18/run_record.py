"""Write down everything needed to reproduce a run."""
import hashlib
import json
import platform
import numpy, scipy, qiskit, qiskit_aer, qiskit_ibm_runtime
from qiskit import qasm3
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez
from tfim_model import trotter

backend = FakeFez()
seed_transpiler, seed_simulator, shots = 11, 1234, 4000
chain = [124, 123, 136, 143, 142, 141]      # the capstone line
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, initial_layout=chain,
    seed_transpiler=seed_transpiler)
qc = trotter(4)
qc.measure_all()
isa = pm.run(qc)
fingerprint = hashlib.sha256(qasm3.dumps(isa).encode()).hexdigest()

record = {"python": platform.python_version()}
for module in [qiskit, qiskit_aer, qiskit_ibm_runtime, numpy, scipy]:
    record[module.__name__] = module.__version__
record |= {
    "backend": f"{backend.name} {backend.backend_version}",
    "calibration": str(backend.properties().last_update_date),
    "seeds": {"transpiler": seed_transpiler,
              "simulator": seed_simulator},
    "shots": shots,
    "layout": isa.layout.final_index_layout(),
    "isa_circuit_sha256": fingerprint[:16],
}
for key, value in record.items():
    print(f"{key:19s}: {value}")
with open("run_record.json", "w") as f:  # keep next to your results
    json.dump(record, f, indent=2)
