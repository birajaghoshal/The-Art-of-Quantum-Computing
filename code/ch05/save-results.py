# Save counts together with everything needed to reproduce them.
import json
import platform
import qiskit
from qiskit import qasm3
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SEED, SHOTS = 2026, 1000
qc = QuantumCircuit(1)
qc.ry(1.2, 0)
qc.measure_all()
res = StatevectorSampler(seed=SEED).run([qc], shots=SHOTS).result()

record = {
    "experiment": "ry(1.2) single-qubit test",
    "counts": dict(sorted(res[0].data.meas.get_counts().items())),
    "shots": SHOTS,
    "seed": SEED,
    "simulator": "StatevectorSampler",
    "qiskit": qiskit.__version__,
    "python": platform.python_version(),
    "circuit_qasm3": qasm3.dumps(qc),
}
path = "code/ch05/ry-test-record.json"
with open(path, "w") as f:
    json.dump(record, f, indent=2)

with open(path) as f:                      # read it back
    loaded = json.load(f)
print("saved keys:", list(loaded))
print("counts:", loaded["counts"], " qiskit", loaded["qiskit"])
