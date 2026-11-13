# A 4-variable SAT formula and a Grover oracle built from its clauses
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCXGate

# (x0 or x1) and (not x0 or x2) and (not x1 or x3)
#   and (not x2 or not x3)
# Each literal is (variable, True for x, False for "not x").
CLAUSES = [[(0, True), (1, True)], [(0, False), (2, True)],
           [(1, False), (3, True)], [(2, False), (3, False)]]

def satisfied(x):
    """Classical check; bit i of the integer x is variable x_i."""
    return all(any(((x >> v) & 1) == pos for v, pos in clause)
               for clause in CLAUSES)

def clause_layer(var, cl):
    """Write each clause's truth value into its own ancilla."""
    qc = QuantumCircuit(var, cl)
    for j, clause in enumerate(CLAUSES):
        flips = [var[v] for v, pos in clause if pos]
        if flips:
            qc.x(flips)              # control on "literal is false"
        qc.append(MCXGate(len(clause)), [var[v] for v, _ in clause]
                  + [cl[j]])         # cl[j] = 1 if clause is FALSE
        if flips:
            qc.x(flips)
        qc.x(cl[j])                 # now cl[j] = 1 if clause is TRUE
    return qc

def sat_oracle():
    """Phase -1 on satisfying inputs (out qubit starts in |->)."""
    var = QuantumRegister(4, "x")
    cl = QuantumRegister(len(CLAUSES), "cl")  # one per clause
    out = QuantumRegister(1, "out")
    qc = QuantumCircuit(var, cl, out, name="SAT oracle")
    layer = clause_layer(var, cl)
    qc.compose(layer, [*var, *cl], inplace=True)       # compute
    qc.append(MCXGate(len(CLAUSES)), [*cl, out[0]])     # AND -> kick
    qc.compose(layer.inverse(), [*var, *cl], inplace=True)  # undo
    return qc

if __name__ == "__main__":
    sols = [format(x, "04b") for x in range(16) if satisfied(x)]
    print("satisfying assignments (x3 x2 x1 x0):", sols)
