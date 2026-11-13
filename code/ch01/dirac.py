# Kets, bras, brackets and outer products as NumPy arrays
import numpy as np
np.set_printoptions(precision=4, suppress=True)

ket0 = np.array([[1], [0]])                 # column vectors
ket1 = np.array([[0], [1]])
plus = (ket0 + ket1) / np.sqrt(2)
psi = 0.6 * ket0 + 0.8 * ket1

def bra(ket):
    return ket.conj().T                     # row vector

print("<+|psi>       =", round((bra(plus) @ psi).item(), 4))

P0 = ket0 @ bra(ket0)                       # outer product |0><0|
P1 = ket1 @ bra(ket1)
print("|0><0|+|1><1| =\n", P0 + P1)
flip = ket0 @ bra(ket1)                     # |0><1|
print("|0><1| |1>    =", (flip @ ket1).ravel())

Pp = plus @ bra(plus)                       # projector onto |+>
print("|+><+|        =\n", Pp)
print("projector squared equals itself?", np.allclose(Pp @ Pp, Pp))
print("<psi|P+|psi>  =", round((bra(psi) @ Pp @ psi).item(), 4))
