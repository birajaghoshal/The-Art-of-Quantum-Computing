# e^{i theta}: a unit complex number that rotates what it multiplies
import numpy as np
np.set_printoptions(precision=3, suppress=True, linewidth=66)

theta = np.pi / 3
u = np.exp(1j * theta)
print("u = e^{i pi/3}   =", np.round(u, 4),
      " |u| =", round(abs(u), 4))

z = 2 + 1j
print(f"z               = {z},  |z| = {abs(z):.4f},"
      f" angle = {np.angle(z):.4f}")
uz = u * z
print(f"u z             = {np.round(uz, 4)},"
      f"  |uz| = {abs(uz):.4f}, angle = {np.angle(uz):.4f}")
print(f"angle increased by {np.angle(uz) - np.angle(z):.4f}"
      f" (pi/3 = {np.pi / 3:.4f})")

# The N-th roots of unity: powers of omega = e^{2 pi i / N}
N = 8
omega = np.exp(2j * np.pi / N)
roots = omega ** np.arange(N)
print("8th roots of unity:")
print(np.round(roots, 3) + 0)
print("omega^8         =", np.round(omega ** N, 10) + 0)
print("sum of roots    =", np.round(roots.sum(), 10) + 0)
