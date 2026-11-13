# The modular multiplier U|y> = |7y mod 15> as a permutation matrix
import numpy as np
from qiskit.quantum_info import Operator, Statevector

a, N, n = 7, 15, 4                  # 4 work qubits hold y = 0..15
U = np.zeros((2**n, 2**n))
for y in range(2**n):
    target = (a * y) % N if y < N else y   # leave y >= N alone
    U[target, y] = 1
print("unitary:", Operator(U).is_unitary())

# Follow the orbit of |1> under repeated multiplication by 7
y, orbit = 1, [1]
while True:
    y = (a * y) % N
    if y == 1:
        break
    orbit.append(y)
r = len(orbit)
print("orbit of 1:", orbit, "-> order r =", r)

# Build |u_s> for s = 1 and test U|u_s> = e^{2 pi i s/r} |u_s>
s = 1
u = np.zeros(2**n, dtype=complex)
for k, yk in enumerate(orbit):
    u[yk] = np.exp(-2j * np.pi * s * k / r) / np.sqrt(r)
Uu = Statevector(u).evolve(Operator(U)).data
ratio = np.round(Uu[1] / u[1], 6) + 0   # "+ 0" tidies a -0.0
phase = np.angle(ratio) / (2 * np.pi)
print(f"eigenvalue = {ratio:.4f}, phase = {phase:.4f}")

# (1/sqrt r) * (sum of all |u_s>) should be |1>: amplitudes on orbit
k = np.arange(r)
total = sum(np.exp(-2j * np.pi * s * k / r) for s in range(r)) / r
print("amplitudes on", orbit, ":", np.abs(np.round(total, 6)))
