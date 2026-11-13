# Print the versions of everything this book depends on.
import platform
import qiskit
import qiskit_aer
import qiskit_ibm_runtime

found = {"qiskit": qiskit.__version__,
         "qiskit-aer": qiskit_aer.__version__,
         "qiskit-ibm-runtime": qiskit_ibm_runtime.__version__}
pinned = {"qiskit": "2.6.1", "qiskit-aer": "0.18.0",
          "qiskit-ibm-runtime": "0.51.0"}

print(f"{'Python':20s}{platform.python_version()}")
for name, version in found.items():
    print(f"{name:20s}{version}")
print("Matches the book's pinned versions:", found == pinned)
