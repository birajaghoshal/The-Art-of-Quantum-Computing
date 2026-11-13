# Spherical coordinates on the unit sphere and back again
import numpy as np

def to_xyz(theta, phi):
    """Unit-sphere point from polar angle theta and azimuth phi."""
    return np.array([np.sin(theta) * np.cos(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(theta)])

def to_angles(p):
    """Recover (theta, phi) from a point on the unit sphere."""
    x, y, z = p
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x) % (2 * np.pi)
    return theta, phi

print(" theta   phi  ->   x       y       z")
for th, ph in [(0, 0), (90, 0), (90, 90), (60, 45), (180, 0)]:
    p = np.round(to_xyz(np.deg2rad(th), np.deg2rad(ph)), 4) + 0.0
    print(f"{th:5d} {ph:5d}  -> {p[0]:+.4f} {p[1]:+.4f} {p[2]:+.4f}")

p = to_xyz(np.deg2rad(60), np.deg2rad(45))
th, ph = to_angles(p)
print(f"round trip: theta = {np.rad2deg(th):.1f} deg,"
      f" phi = {np.rad2deg(ph):.1f} deg,"
      f" |p| = {np.linalg.norm(p):.4f}")
