"""Five single-qubit noise channels: Kraus form and effect."""
import numpy as np
from qiskit.quantum_info import DensityMatrix, Kraus, Pauli
from qiskit_aer.noise import (pauli_error, depolarizing_error,
                              amplitude_damping_error,
                              thermal_relaxation_error)

p = 0.2
channels = {
    "bit flip": pauli_error([("X", p), ("I", 1 - p)]),
    "phase flip": pauli_error([("Z", p), ("I", 1 - p)]),
    "depolarising": depolarizing_error(p, 1),
    "amp. damping": amplitude_damping_error(p),
    # T1 = 50 us, T2 = 40 us, idle for 10 us
    "thermal": thermal_relaxation_error(50e-6, 40e-6, 10e-6),
}

def bloch(rho):
    vals = [rho.expectation_value(Pauli(s)).real for s in "XYZ"]
    return [round(v, 6) + 0.0 for v in vals]  # avoid -0.000

plus = DensityMatrix.from_label("+")
one = DensityMatrix.from_label("1")
print(f"{'channel':13s} #K  sum K^+K=I   |+> Bloch (x,z)  |1> z")
for name, err in channels.items():
    kraus = Kraus(err.to_quantumchannel())
    ops = kraus.data
    total = sum(K.conj().T @ K for K in ops)
    ok = np.allclose(total, np.eye(2))
    x, _, z = bloch(plus.evolve(kraus))
    z1 = bloch(one.evolve(kraus))[2]
    print(f"{name:13s} {len(ops):2d}  {str(ok):10s}"
          f"  ({x:+.3f}, {z:+.3f})   {z1:+.3f}")
