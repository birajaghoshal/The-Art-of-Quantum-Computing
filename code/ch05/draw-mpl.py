# Save a publication-quality drawing of the three-coin circuit.
from math import pi
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.x(1)
qc.ry(2 * pi / 3, 2)
qc.measure_all()

fig = qc.draw("mpl")
fig.savefig("figures/ch05/first-circuit.pdf", bbox_inches="tight")
print("saved figures/ch05/first-circuit.pdf")
