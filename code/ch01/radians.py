# Degrees, radians and points on the unit circle
import numpy as np

def tidy(x):
    """Round to 4 decimals and turn -0.0 into 0.0."""
    return np.round(x, 4) + 0.0

degrees = [0, 30, 45, 90, 180, 270]
for d in degrees:
    r = np.deg2rad(d)               # same as d * pi / 180
    print(f"{d:3d} deg = {r:.4f} rad   (cos, sin) = "
          f"({tidy(np.cos(r)):+.4f}, {tidy(np.sin(r)):+.4f})")
