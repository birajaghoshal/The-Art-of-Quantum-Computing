# Phase kickback: the control picks up the phase, not the target
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace

for target in ["0", "1"]:
    qc = QuantumCircuit(2)
    qc.h(0)                          # control q0 in |+>
    if target == "1":
        qc.x(1)                      # target q1 in |1>
    qc.cp(np.pi / 2, 0, 1)           # controlled phase of pi/2

    psi = Statevector(qc)
    rho_c = partial_trace(psi, [1])  # trace out the target
    rho_t = partial_trace(psi, [0])  # trace out the control
    phase = np.angle(rho_c.data[1, 0]) / np.pi
    p_t1 = rho_t.probabilities()[1]
    print(f"target |{target}>: P(t=1) = {p_t1:.3f},"
          f" purity(c) = {rho_c.purity().real:.3f},"
          f" phase(c) = {phase:.3f} pi")
