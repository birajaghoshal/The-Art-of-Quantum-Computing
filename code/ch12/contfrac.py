# Continued fractions with exact rational arithmetic
from fractions import Fraction

def cf_terms(x):
    """Continued-fraction terms [a0; a1, a2, ...] of a Fraction."""
    terms = []
    while True:
        a = x.numerator // x.denominator
        terms.append(a)
        x = x - a
        if x == 0:
            return terms
        x = 1 / x

def convergents(terms):
    """The successive truncations a0, a0 + 1/a1, ... as Fractions."""
    out = []
    for k in range(1, len(terms) + 1):
        value = Fraction(terms[k - 1])
        for a in reversed(terms[:k - 1]):
            value = a + 1 / value
        out.append(value)
    return out

x = Fraction(853, 1024)        # a 10-bit measured phase
print("x =", x, "=", round(float(x), 6))
print("terms:", cf_terms(x))
for c in convergents(cf_terms(x)):
    print(f"  convergent {str(c):>9}  error {float(abs(x - c)):.6f}")
print("limit_denominator(21):", x.limit_denominator(21))
