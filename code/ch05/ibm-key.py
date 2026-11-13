# norun
# Run ONCE on your own computer to store your IBM Quantum key.
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="PASTE-YOUR-API-KEY-HERE",      # never commit this to git
    instance="PASTE-YOUR-INSTANCE-CRN",   # from your IBM Quantum
    set_as_default=True,                  # dashboard
)
service = QiskitRuntimeService()          # loads the saved account
for b in service.backends():
    print(b.name, b.num_qubits, "qubits")
