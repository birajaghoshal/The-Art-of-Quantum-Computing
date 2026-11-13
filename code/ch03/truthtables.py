"""Truth tables for basic Boolean gates and a half adder."""
from itertools import product

gates = {
    "AND":  lambda a, b: a & b,
    "OR":   lambda a, b: a | b,
    "XOR":  lambda a, b: a ^ b,
    "NAND": lambda a, b: 1 - (a & b),
}

# One row per input pair, one column per gate
print("a b | " + " ".join(f"{g:>4}" for g in gates))
print("-" * 26)
for a, b in product([0, 1], repeat=2):
    outs = " ".join(f"{f(a, b):>4}" for f in gates.values())
    print(f"{a} {b} | {outs}")

# A half adder adds two bits: sum = a XOR b, carry = a AND b
print("\nHalf adder")
print("a b | carry sum | a+b")
for a, b in product([0, 1], repeat=2):
    s, c = a ^ b, a & b
    print(f"{a} {b} |   {c}    {s}  |  {2 * c + s}")
