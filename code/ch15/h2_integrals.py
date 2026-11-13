"""Companion script: STO-3G integrals for H2 from scratch.

Regenerates the molecular integrals used in h2_exact.py and the
coefficient table in h2_curve.py. Only s-type Gaussians are needed,
so every integral has a closed form (Szabo and Ostlund, Appendix A).
"""
import numpy as np
from scipy.special import erf

ALPHA = np.array([3.42525091, 0.62391373, 0.16885540])  # zeta = 1.24
COEF = np.array([0.15432897, 0.53532814, 0.44463454])
NORM = COEF * (2 * ALPHA / np.pi) ** 0.75
BOHR = 1.8897261246  # bohr per angstrom


def f0(t):
    return 1.0 if t < 1e-10 else 0.5 * np.sqrt(np.pi / t) * erf(np.sqrt(t))


def prims(A):
    return [(a, d, A) for a, d in zip(ALPHA, NORM)]


def one_e(fa, fb, nuclei):
    S = T = V = 0.0
    for a, da, A in fa:
        for b, db, B in fb:
            p, ab2 = a + b, (A - B) ** 2
            P = (a * A + b * B) / p
            k = np.exp(-a * b / p * ab2)
            S += da * db * (np.pi / p) ** 1.5 * k
            T += da * db * a * b / p * (3 - 2 * a * b / p * ab2) \
                * (np.pi / p) ** 1.5 * k
            for C in nuclei:
                V += -da * db * 2 * np.pi / p * k * f0(p * (P - C) ** 2)
    return S, T + V


def eri(fa, fb, fc, fd):
    total = 0.0
    for a, da, A in fa:
        for b, db, B in fb:
            p, P = a + b, (a * A + b * B) / (a + b)
            kab = np.exp(-a * b / p * (A - B) ** 2)
            for c, dc, C in fc:
                for d, dd, D in fd:
                    q, Q = c + d, (c * C + d * D) / (c + d)
                    kcd = np.exp(-c * d / q * (C - D) ** 2)
                    total += da * db * dc * dd * 2 * np.pi ** 2.5 \
                        / (p * q * np.sqrt(p + q)) * kab * kcd \
                        * f0(p * q / (p + q) * (P - Q) ** 2)
    return total


def h2_integrals(R_angstrom):
    R = R_angstrom * BOHR
    fA, fB = prims(0.0), prims(R)
    S, hAA = one_e(fA, fA, [0.0, R])
    _, hAB = one_e(fA, fB, [0.0, R])
    S = one_e(fA, fB, [0.0, R])[0]
    # bonding (g) and antibonding (u) orbitals fixed by symmetry
    cg, cu = 1 / np.sqrt(2 * (1 + S)), 1 / np.sqrt(2 * (1 - S))
    h_gg, h_uu = 2 * cg**2 * (hAA + hAB), 2 * cu**2 * (hAA - hAB)
    f, idx = [fA, fB], [0, 1]
    g = np.zeros((2, 2, 2, 2))
    for i in idx:
        for j in idx:
            for k in idx:
                for m in idx:
                    g[i, j, k, m] = eri(f[i], f[j], f[k], f[m])
    C = np.array([[cg, cu], [cg, -cu]])  # columns: g, u
    mo = np.einsum("pi,qj,rk,sl,pqrs->ijkl", C, C, C, C, g)
    return dict(h_gg=h_gg, h_uu=h_uu, J_gg=mo[0, 0, 0, 0],
                J_uu=mo[1, 1, 1, 1], J_gu=mo[0, 0, 1, 1],
                K_gu=mo[0, 1, 0, 1], E_nuc=1 / R)


def coefficients(I):
    E_gg = 2 * I["h_gg"] + I["J_gg"]
    E_uu = 2 * I["h_uu"] + I["J_uu"]
    E_gu = I["h_gg"] + I["h_uu"] + I["J_gu"]
    c0 = (E_gg + E_uu) / 4 + E_gu / 2
    c1 = (E_uu - E_gg) / 4
    c3 = -(E_gg + E_uu - 2 * E_gu) / 4
    return c0, c1, c3, I["K_gu"], I["E_nuc"]


if __name__ == "__main__":
    I = h2_integrals(0.735)
    print("Integrals at 0.735 angstrom (hartree):")
    for key, val in I.items():
        print(f"  {key:6s} {val: .7f}")
    print("R      c0        c1       c3        c4       E_nuc")
    for R in [0.35, 0.45, 0.55, 0.65, 0.735, 0.85, 1.0, 1.2,
              1.5, 2.0, 2.5, 3.0]:
        c0, c1, c3, c4, en = coefficients(h2_integrals(R))
        print(f"{R:<5} {c0: .5f} {c1: .5f} {c3: .5f} {c4: .5f} {en: .5f}")
