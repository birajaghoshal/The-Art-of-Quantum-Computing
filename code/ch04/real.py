# norun
"""Run the scripts of this section on a real device."""
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
print("Device:", backend.name, "with", backend.num_qubits, "qubits")
