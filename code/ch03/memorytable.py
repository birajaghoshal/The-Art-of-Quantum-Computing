"""Memory needed to store a full n-qubit state vector:
2**n complex amplitudes, 16 bytes each (two 64-bit floats)."""
from qiskit.quantum_info import Statevector

UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]

def human(nbytes):
    i = min((nbytes.bit_length() - 1) // 10, len(UNITS) - 1)
    return f"{nbytes / 1024**i:,.0f} {UNITS[i]}"

print(f"{'qubits':>6} {'amplitudes':>20} {'memory':>10}")
for n in range(10, 51, 10):
    print(f"{n:>6} {2**n:>20,} {human(16 * 2**n):>10}")

# Check the formula against a real Statevector object
sv = Statevector.from_label("0" * 20)
print("\n20-qubit Statevector uses", human(sv.data.nbytes))
n_max = max(n for n in range(64) if 16 * 2**n <= 16 * 1024**3)
print("Largest n that fits in 16 GiB:", n_max)
