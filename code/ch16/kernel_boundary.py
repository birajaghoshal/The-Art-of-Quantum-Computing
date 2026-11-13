"""Decision regions of the ZZ-kernel SVM on the moons data."""
import numpy as np
from qiskit.circuit.library import zz_feature_map
from sklearn.svm import SVC
from moons_data import load
from fidelity_kernel import feature_states, kernel

Xtr, Xte, ytr, yte = load(top=np.pi / 2)
fmap = zz_feature_map(2, reps=2)
Str = feature_states(fmap, Xtr)
svm = SVC(kernel="precomputed", C=1.0).fit(kernel(Str, Str), ytr)

# Evaluate the classifier on a 45 x 45 grid of new points
g = np.linspace(-0.2, np.pi / 2 + 0.2, 45)
G0, G1 = np.meshgrid(g, g)
grid = np.column_stack([G0.ravel(), G1.ravel()])
Sgrid = feature_states(fmap, grid)
score = svm.decision_function(kernel(Sgrid, Str))
print("grid points classified:", len(grid))
print("kernel entries computed for the grid:", len(grid) * len(Xtr))

# Plotting code for Figure 16.4: see the companion repository.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.contourf(G0, G1, score.reshape(G0.shape), levels=[-9, 0, 9],
            colors=["#1F5FBF", "#F28C28"], alpha=0.18)
ax.contour(G0, G1, score.reshape(G0.shape), levels=[0],
           colors="#5B6B7F")
for c, col in [(0, "#1F5FBF"), (1, "#F28C28")]:
    ax.scatter(*Xtr[ytr == c].T, color=col, s=18)
    ax.scatter(*Xte[yte == c].T, color=col, marker="x", s=30)
sv = Xtr[svm.support_]
ax.scatter(*sv.T, facecolors="none", edgecolors="#2E9E5B", s=70,
           label="support vectors")
ax.set_xlabel("feature $x_0$")
ax.set_ylabel("feature $x_1$")
ax.legend(fontsize=8, loc="lower left")
fig.tight_layout()
fig.savefig("figures/ch16/kernel_boundary.pdf")
