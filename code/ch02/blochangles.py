# From amplitudes to Bloch-sphere angles and coordinates
import numpy as np
from qiskit.quantum_info import Statevector, Pauli

def bloch_angles(psi):
    a, b = psi.data
    b = b * np.exp(-1j * np.angle(a))    # drop the global phase
    theta = 2 * np.arccos(np.clip(abs(a), 0, 1))
    phi = np.angle(b) % (2 * np.pi) if abs(b) > 1e-12 else 0.0
    return theta, phi

def bloch_vector(psi):
    return [psi.expectation_value(Pauli(p)).real for p in "XYZ"]

s = 1 / np.sqrt(2)
states = {"|0>": [1, 0], "|1>": [0, 1], "|+>": [s, s],
          "|->": [s, -s], "|+i>": [s, 1j * s], "|-i>": [s, -1j * s],
          "0.6|0>+0.8i|1>": [0.6, 0.8j]}
print("state          theta/pi phi/pi     x      y      z")
for name, amps in states.items():
    psi = Statevector(amps)
    th, ph = bloch_angles(psi)
    x, y, z = np.round(bloch_vector(psi), 3) + 0.0
    print(f"{name:15s} {th / np.pi:6.3f} {ph / np.pi:6.3f}"
          f"  {x:+.3f} {y:+.3f} {z:+.3f}")
