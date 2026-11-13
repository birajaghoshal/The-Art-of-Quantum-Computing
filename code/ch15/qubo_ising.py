"""Turn a three-variable QUBO into an Ising Hamiltonian; check it."""
from qiskit.quantum_info import SparsePauliOp

# Minimise f = sum_i a_i x_i + sum_{i<j} b_ij x_i x_j, x_i in {0,1}
a = {0: -4.0, 1: -3.0, 2: -5.0}
b = {(0, 1): 1.0, (1, 2): 3.0, (0, 2): 6.0}
n = 3

def f(x):
    return (sum(a[i] * x[i] for i in a)
            + sum(w * x[i] * x[j] for (i, j), w in b.items()))

# Substitute x_i = (1 - z_i)/2, so x_i = 1 <-> z_i = -1 <-> |1>
terms, const = [], 0.0
for i, ai in a.items():
    const += ai / 2
    terms.append(("Z", [i], -ai / 2))
for (i, j), w in b.items():
    const += w / 4
    terms += [("Z", [i], -w / 4), ("Z", [j], -w / 4),
              ("ZZ", [i, j], w / 4)]
terms.append(("", [], const))
H = SparsePauliOp.from_sparse_list(terms, num_qubits=n).simplify()
terms = [f"{c.real:+.2f} {lab}" for lab, c in H.to_list()]
print("H =", "  ".join(terms[:4]))
print("   ", "  ".join(terms[4:]))

diag = H.to_matrix(sparse=True).diagonal().real
print("state  x0 x1 x2   f(x)   <H>")
for k in range(2 ** n):
    x = [(k >> i) & 1 for i in range(n)]     # x_i lives on qubit i
    print(f"|{k:03b}>  {x[0]}  {x[1]}  {x[2]}   {f(x):5.1f}"
          f"  {diag[k]:5.1f}")
