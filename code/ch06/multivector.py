# Four qubits, four different gates, one picture.
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector

qc = QuantumCircuit(4)
qc.x(0)               # q0: north pole -> south pole
qc.h(1)               # q1: north pole -> +x
qc.h(2)
qc.s(2)               # q2: +x -> +y (a quarter turn about z)
qc.rx(pi / 3, 3)      # q3: tilted 60 degrees towards -y

psi = Statevector(qc)
fig = plot_bloch_multivector(psi, font_size=11,
                             title_font_size=11)
fig.set_size_inches(8, 2.4)
fig.savefig("figures/ch06/multivector.pdf", bbox_inches="tight")
print("saved figures/ch06/multivector.pdf")
