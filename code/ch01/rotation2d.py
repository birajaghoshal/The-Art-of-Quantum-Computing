# Rotating vectors in the plane with a 2x2 matrix
import numpy as np

def rot(theta):
    """Matrix that turns a 2D vector anticlockwise by theta."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])

v = np.array([2.0, 1.0])
R = rot(np.pi / 2)                       # a quarter turn
print("R(pi/2) =\n", np.round(R, 4) + 0.0)
print("R(pi/2) v =", np.round(R @ v, 4) + 0.0)

# Two rotations in a row: the angles add
a, b = 0.3, 0.9
print("R(a) R(b) equals R(a+b)?", np.allclose(rot(a) @ rot(b),
                                             rot(a + b)))
# Rotations do not change lengths
w = rot(1.234) @ v
print(f"length before {np.linalg.norm(v):.4f},"
      f" after {np.linalg.norm(w):.4f}")
# The transpose undoes the rotation
print("R^T R equals I?",
      np.allclose(rot(1.234).T @ rot(1.234), np.eye(2)))
