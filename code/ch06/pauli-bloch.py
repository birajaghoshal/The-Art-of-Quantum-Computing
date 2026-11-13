# One state and its images under X, Y and Z on the Bloch sphere.
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.visualization import plot_bloch_vector

def bloch(psi):
    return [float(psi.expectation_value(SparsePauliOp(p)).real)
            for p in "XYZ"]

prep = QuantumCircuit(1)
prep.ry(np.pi / 3, 0)            # polar angle 60 degrees
prep.rz(np.pi / 4, 0)            # azimuth 45 degrees
psi = Statevector(prep)

fig = plt.figure(figsize=(8, 2.4))
for k, gate in enumerate(["start", "x", "y", "z"]):
    qc = QuantumCircuit(1)
    if gate != "start":
        getattr(qc, gate)(0)
    r = bloch(psi.evolve(qc))
    print(f"{gate:5s} r = ({r[0]:+.3f}, {r[1]:+.3f}, {r[2]:+.3f})")
    ax = fig.add_subplot(1, 4, k + 1, projection="3d")
    title = "start" if gate == "start" else f"after {gate.upper()}"
    plot_bloch_vector(r, title=title, ax=ax, font_size=11)
fig.savefig("figures/ch06/pauli-bloch.pdf", bbox_inches="tight")
print("saved figures/ch06/pauli-bloch.pdf")
