"""Parameter and CNOT counts for three library ansatz families."""
from qiskit.circuit.library import (efficient_su2, n_local,
                                    real_amplitudes)

print(" n reps | RealAmp  EffSU2  RY-CZ | CNOTs(RealAmp)")
for n in [2, 4, 6]:
    for reps in [1, 3]:
        ra = real_amplitudes(n, reps=reps)
        su2 = efficient_su2(n, reps=reps)
        ryz = n_local(n, "ry", "cz", entanglement="linear",
                      reps=reps)
        cx = ra.count_ops().get("cx", 0)
        print(f"{n:2d} {reps:4d} | {ra.num_parameters:7d} "
              f"{su2.num_parameters:7d} {ryz.num_parameters:6d}"
              f" | {cx:6d}")
