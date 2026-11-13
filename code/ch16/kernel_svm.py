"""Support vector machines with quantum kernels on the moons data."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import zz_feature_map
from sklearn.svm import SVC
from moons_data import load
from fidelity_kernel import feature_states, kernel

x = ParameterVector("x", 2)
angle_map = QuantumCircuit(2)              # product (angle) encoding
angle_map.ry(x[0], 0)
angle_map.ry(x[1], 1)
maps = {"angle": angle_map, "ZZ, reps=2": zz_feature_map(2, reps=2)}

print("feature map   range  train  test   support vectors")
for top in [np.pi / 2, np.pi, 2 * np.pi]:
    Xtr, Xte, ytr, yte = load(top)
    for name, fmap in maps.items():
        Str = feature_states(fmap, Xtr)
        Ste = feature_states(fmap, Xte)
        svm = SVC(kernel="precomputed", C=1.0)
        svm.fit(kernel(Str, Str), ytr)             # train x train
        tr = svm.score(kernel(Str, Str), ytr)
        te = svm.score(kernel(Ste, Str), yte)      # test x train
        print(f"{name:12s} {top / np.pi:4.1f}pi  {tr:.3f}  {te:.3f}"
              f"   {svm.n_support_.sum():3d}")
