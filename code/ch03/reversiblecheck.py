"""A gate is reversible when no two inputs give the same output."""
from itertools import product

def is_reversible(gate, n):
    inputs = list(product([0, 1], repeat=n))
    return len({gate(*bits) for bits in inputs}) == len(inputs)

gates = {
    "AND (2 in, 1 out)": (lambda a, b: (a & b,), 2),
    "CNOT":              (lambda a, b: (a, a ^ b), 2),
    "AND kept inputs":   (lambda a, b: (a, b, a & b), 2),
    "Toffoli":           (lambda a, b, c: (a, b, c ^ (a & b)), 3),
}
for name, (g, n) in gates.items():
    print(f"{name:<18} reversible: {is_reversible(g, n)}")
