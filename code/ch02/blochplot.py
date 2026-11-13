# Draw one state on the Bloch sphere with Qiskit's plotting helper
import numpy as np
from qiskit.quantum_info import Statevector, Pauli
from qiskit.visualization import plot_bloch_vector

psi = Statevector([0.6, 0.8j])
xyz = [psi.expectation_value(Pauli(p)).real for p in "XYZ"]
print("Bloch vector:", np.round(xyz, 4) + 0.0)

fig = plot_bloch_vector(xyz, title="0.6|0> + 0.8i|1>",
                        figsize=(3.6, 3.6))
fig.savefig("figures/ch02/bloch_qiskit.pdf", bbox_inches="tight")
print("saved figures/ch02/bloch_qiskit.pdf")
