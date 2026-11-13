"""Apply a weak noise channel again and again and watch the qubit."""
from qiskit.quantum_info import DensityMatrix, Kraus, Pauli
from qiskit_aer.noise import (pauli_error, depolarizing_error,
                              amplitude_damping_error)

p, steps = 0.05, 40
channels = {
    "bit flip": pauli_error([("X", p), ("I", 1 - p)]),
    "phase flip": pauli_error([("Z", p), ("I", 1 - p)]),
    "depolarising": depolarizing_error(p, 1),
    "amplitude damping": amplitude_damping_error(p),
}
for name, err in channels.items():
    K, final = Kraus(err.to_quantumchannel()), []
    # coherence <X> of |+>, and population <Z> of |1>
    for label, obs in [("+", "X"), ("1", "Z")]:
        rho = DensityMatrix.from_label(label)
        for _ in range(steps):
            rho = rho.evolve(K)
        final.append(rho.expectation_value(Pauli(obs)).real)
    print(f"{name:17s} final <X> = {final[0]:+.3f}   "
          f"final <Z> = {final[1]:+.3f}")
