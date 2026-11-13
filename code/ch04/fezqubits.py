"""Coherence times and error rates for the first few qubits."""
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
target = backend.target

print("qubit   T1 (us)   T2 (us)   sx error   readout error")
for q in range(6):
    props = backend.qubit_properties(q)   # T1, T2 in seconds
    sx_err = target["sx"][(q,)].error
    ro_err = target["measure"][(q,)].error
    print(f"{q:>5} {props.t1 * 1e6:>9.1f} {props.t2 * 1e6:>9.1f}"
          f" {sx_err:>10.5f} {ro_err:>14.4f}")

# Durations are stored in seconds; convert to nanoseconds
print("\nsx duration (ns):     ", target["sx"][(0,)].duration * 1e9)
print("cz duration (ns), 0-1:", target["cz"][(0, 1)].duration * 1e9)
print("measure duration (ns):",
      target["measure"][(0,)].duration * 1e9)
