# Simulating Stern-Gerlach filters with the measurement rules
import numpy as np

rng = np.random.default_rng(42)
Z = (np.array([1, 0]), np.array([0, 1]))               # up, down
X = (np.array([1, 1]) / np.sqrt(2), np.array([1, -1]) / np.sqrt(2))

def measure(state, basis):
    """Born rule, then collapse onto the basis vector found."""
    probs = [abs(np.vdot(b, state)) ** 2 for b in basis]
    k = rng.choice(2, p=probs)
    return k, basis[k]

atoms = 2000
zz = zxz_pass = zxz_down = 0
for _ in range(atoms):
    k, _ = measure(Z[0], Z)          # Z-up atom, a second Z magnet
    zz += k
    k, state = measure(Z[0], X)      # Z-up atom meets an X magnet
    if k == 0:                       # keep only the X-plus beam
        zxz_pass += 1
        k, state = measure(state, Z) # and a final Z magnet
        zxz_down += k
print(f"Z then Z   : {zz} of {atoms} atoms come out 'down'")
print(f"Z then X   : {zxz_pass} of {atoms} pass the X+ filter")
print(f"then Z     : {zxz_down} of those {zxz_pass} come out 'down'")
