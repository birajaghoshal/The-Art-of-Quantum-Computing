"""A variational quantum classifier, written by hand."""
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import real_amplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from moons_data import load

OBS = SparsePauliOp("IZ")            # read out Z on qubit 0
est = StatevectorEstimator()

def predict(qc, w, X):
    # Parameters sort as w[...] then x[...]: weights first, data last
    vals = np.hstack([np.tile(w, (len(X), 1)), X])
    return est.run([(qc, OBS, vals)]).result()[0].data.evs

def train(qc, X, y, maxiter, seed=0):
    t = 2 * y - 1                    # labels 0/1 -> targets -1/+1
    history = []
    def loss(w):                     # mean squared error
        history.append(np.mean((predict(qc, w, X) - t) ** 2))
        return history[-1]
    rng = np.random.default_rng(seed)
    w0 = rng.uniform(-1, 1, qc.num_parameters - X.shape[1])
    res = minimize(loss, w0, method="COBYLA",
                   options={"maxiter": maxiter})
    return res.x, history

def accuracy(qc, w, X, y):
    return np.mean((predict(qc, w, X) > 0) == (y == 1))

if __name__ == "__main__":
    x = ParameterVector("x", 2)
    qc = QuantumCircuit(2)
    qc.ry(x[0], 0)                   # angle encoding, done once
    qc.ry(x[1], 1)
    qc.compose(real_amplitudes(2, reps=2, parameter_prefix="w"),
               inplace=True)
    print("parameter order:", [p.name for p in qc.parameters])
    Xtr, Xte, ytr, yte = load()
    w, hist = train(qc, Xtr, ytr, maxiter=150)
    print(f"loss: start {hist[0]:.4f}, end {hist[-1]:.4f}, "
          f"evaluations {len(hist)}")
    print(f"train accuracy {accuracy(qc, w, Xtr, ytr):.3f}")
    print(f"test accuracy  {accuracy(qc, w, Xte, yte):.3f}")
