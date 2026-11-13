# A first look: a qubit state, a gate and measurement probabilities
import numpy as np

# A qubit state is a pair of complex numbers (amplitudes)
state = np.array([3 / 5, 4j / 5])
print("state        =", state)

# A gate is a 2x2 matrix; this one is called the Hadamard matrix
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
new_state = H @ state
print("H @ state    =", np.round(new_state, 4))

# Measurement probabilities are squared magnitudes
for name, s in [("before", state), ("after", new_state)]:
    p = np.abs(s) ** 2
    print(f"{name:6s}: P(0) = {p[0]:.4f}, P(1) = {p[1]:.4f},"
          f" total = {p.sum():.4f}")
