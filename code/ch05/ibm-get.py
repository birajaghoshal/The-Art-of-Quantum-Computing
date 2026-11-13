# norun
# Fetch the results of an earlier job by its id.
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
job = service.job("PASTE-YOUR-JOB-ID")
print("status:", job.status())
result = job.result()
print(dict(sorted(result[0].data.meas.get_counts().items())))
print("usage:", job.usage(), "seconds of QPU time")
