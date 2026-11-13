"""Small helpers for testing circuits (Chapter 9)."""
from qiskit.quantum_info import Statevector
from scipy.stats import chisquare

def rotate_to(qc, basis):
    """Copy of qc ready to measure in basis, written "q1 q0"."""
    out = qc.copy()
    for q, b in enumerate(reversed(basis)):
        if b == "X":
            out.h(q)
        elif b == "Y":
            out.sdg(q); out.h(q)
    return out

def exact_probs(qc, basis):
    return Statevector(rotate_to(qc, basis)).probabilities_dict()

def sample_counts(qc, basis, sampler, shots):
    m = rotate_to(qc, basis)
    m.measure_all()
    res = sampler.run([m], shots=shots).result()[0]
    return dict(sorted(res.data.meas.get_counts().items()))

def fits(counts, probs, alpha=1e-3):
    """Chi-square fit test. Impossible outcomes fail at once."""
    keys = [k for k, p in probs.items() if p > 1e-12]
    if any(k not in keys for k in counts):
        return False
    n = sum(counts.values())
    obs = [counts.get(k, 0) for k in keys]
    return len(keys) == 1 or bool(chisquare(
        obs, [n * probs[k] for k in keys]).pvalue > alpha)
