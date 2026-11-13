"""Data re-uploading: load the features again in every layer."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from moons_data import load
from vqc import accuracy, predict, train

def reupload_circuit(layers):
    x = ParameterVector("x", 2)
    w = ParameterVector("w", 4 * layers)
    qc = QuantumCircuit(2)
    for k in range(layers):
        qc.ry(x[0], 0)               # load the data (again)
        qc.ry(x[1], 1)
        qc.ry(w[4 * k], 0)           # trainable rotations
        qc.ry(w[4 * k + 1], 1)
        qc.rz(w[4 * k + 2], 0)
        qc.rz(w[4 * k + 3], 1)
        qc.cz(0, 1)                  # entangle
    return qc

qc = reupload_circuit(3)
Xtr, Xte, ytr, yte = load()
w, hist = train(qc, Xtr, ytr, maxiter=300)
print(f"weights: {len(w)}, loss evaluations: {len(hist)}")
print(f"loss: start {hist[0]:.4f}, end {hist[-1]:.4f}")
print(f"train accuracy {accuracy(qc, w, Xtr, ytr):.3f}")
print(f"test accuracy  {accuracy(qc, w, Xte, yte):.3f}")

# Plotting code for Figure 16.5: see the companion repository.
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.4, 3.0))
a1.plot(hist, color="#7B4FBF")
a1.set_xlabel("loss evaluation")
a1.set_ylabel("training loss (MSE)")
g = np.linspace(-0.3, np.pi + 0.3, 40)
G0, G1 = np.meshgrid(g, g)
f = predict(qc, w, np.column_stack([G0.ravel(), G1.ravel()]))
a2.contourf(G0, G1, f.reshape(G0.shape), levels=[-1, 0, 1],
            colors=["#1F5FBF", "#F28C28"], alpha=0.18)
for c, col in [(0, "#1F5FBF"), (1, "#F28C28")]:
    a2.scatter(*Xtr[ytr == c].T, color=col, s=12)
    a2.scatter(*Xte[yte == c].T, color=col, marker="x", s=24)
a2.set_xlabel("$x_0$")
a2.set_ylabel("$x_1$")
fig.tight_layout()
fig.savefig("figures/ch16/vqc_reupload.pdf")
