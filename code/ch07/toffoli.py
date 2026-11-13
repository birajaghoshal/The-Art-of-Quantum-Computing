# Toffoli from CNOTs, H, T and Tdg, checked against qc.ccx
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

a, b, t = 0, 1, 2                # controls a, b and target t
qc = QuantumCircuit(3)
qc.h(t)
qc.cx(b, t); qc.tdg(t)
qc.cx(a, t); qc.t(t)
qc.cx(b, t); qc.tdg(t)
qc.cx(a, t); qc.t(b); qc.t(t)
qc.h(t)
qc.cx(a, b); qc.t(a); qc.tdg(b)
qc.cx(a, b)

ref = QuantumCircuit(3)
ref.ccx(a, b, t)
print("Decomposition equals Toffoli:",
      Operator(qc).equiv(Operator(ref)))
print("Gate counts:", dict(sorted(qc.count_ops().items())))
print("Depth:", qc.depth())

fig = qc.draw("mpl", fold=-1, scale=0.8)
fig.savefig("figures/ch07/toffoli_decomp.pdf", bbox_inches="tight")
