from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def rref_mod2(rows):
    """Row-reduce 0/1 rows mod 2; return reduced rows and pivots."""
    m, pivots, r = [row[:] for row in rows], [], 0
    for col in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][col]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][col]:
                m[i] = [a ^ b for a, b in zip(m[i], m[r])]
        pivots.append(col)
        r += 1
    return m[:r], pivots

s, n = "1011", 4                         # the hidden period
bits = [int(b) for b in reversed(s)]
qc = QuantumCircuit(2 * n, n)
qc.h(range(n))
for q in range(n):
    qc.cx(q, n + q)
for q in range(n):
    if bits[q]:
        qc.cx(bits.index(1), n + q)
qc.h(range(n))
qc.measure(range(n), range(n))

shots = StatevectorSampler(seed=7).run([qc], shots=20).result()
eqs, used = [], 0
for y in shots[0].data.c.get_bitstrings():   # one query per shot
    used += 1
    row = [int(b) for b in y]                # columns: s3 s2 s1 s0
    if len(rref_mod2(eqs + [row])[0]) > len(eqs):
        eqs.append(row)
        terms = [f"s{n-1-j}" for j in range(n) if row[j]]
        print(f"run {used:2d}: y = {y}  ->  {' + '.join(terms)} = 0")
    if len(eqs) == n - 1:
        break

red, piv = rref_mod2(eqs)
free = [c for c in range(n) if c not in piv][0]
guess = [0] * n
guess[free] = 1                          # set the free unknown to 1
for row, p in zip(red, piv):
    guess[p] = row[free]                 # pivot = free value (mod 2)
print("reduced rows:", ["".join(map(str, r)) for r in red])
print("recovered s =", "".join(map(str, guess)), " true s =", s)
