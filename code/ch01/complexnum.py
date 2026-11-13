# Complex arithmetic in Python and NumPy
import numpy as np

z = 3 + 4j                 # Python writes i as j
w = 1 - 2j
print("z + w     =", z + w)
print("z * w     =", z * w)
print("z / w     =", z / w)
print("conj(z)   =", np.conj(z))
print("|z|       =", abs(z))
print("z conj(z) =", z * np.conj(z))

# Polar form: modulus r and angle (argument) phi
r, phi = abs(z), np.angle(z)
print(f"polar     : r = {r:.4f}, phi = {phi:.4f} rad")
print("rebuilt   =", np.round(r * np.exp(1j * phi), 4))

# The dtype decides whether NumPy works with complex numbers
a = np.array([-4.0])
b = np.array([-4.0], dtype=complex)
print("sqrt of real   -4:", np.sqrt(a), " dtype", a.dtype)
print("sqrt of complex -4:", np.sqrt(b), " dtype", b.dtype)
