from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def simon_oracle(s):
    """|x>|y> -> |x>|y XOR f(x)> with f(x) = f(x XOR s)."""
    n = len(s)
    bits = [int(b) for b in reversed(s)]     # bits[q] for qubit q
    qc = QuantumCircuit(2 * n, name="O_f")
    for q in range(n):
        qc.cx(q, n + q)                      # copy x into y
    p = bits.index(1)                        # lowest set bit of s
    for q in range(n):
        if bits[q]:
            qc.cx(p, n + q)                  # add x_p * s to y
    return qc

s, n = "1011", 4
oracle = simon_oracle(s)
seen = set()
for x in range(2 ** n):
    if x in seen:
        continue
    partner = x ^ int(s, 2)
    seen.update({x, partner})
    out = []
    for inp in (x, partner):
        sv = Statevector.from_int(inp, 2 ** (2 * n)).evolve(oracle)
        key = max(sv.probabilities_dict().items(),
                  key=lambda t: t[1])
        out.append(key[0][:n])               # y = top n bits
    print(f"f({x:04b}) = {out[0]}   f({partner:04b}) = {out[1]}")
