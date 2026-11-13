"""Typical error and timing numbers of the FakeFez device model."""
import numpy as np
from qiskit_ibm_runtime.fake_provider import FakeFez

target = FakeFez().target

def median_error(name):
    # Skip entries with error >= 1: they flag broken couplers
    errs = [p.error for p in target[name].values()
            if p is not None and p.error is not None
            and p.error < 1]
    return np.median(errs)

def median_time(name):
    return np.median([p.duration for p in target[name].values()])

t1 = np.median([q.t1 for q in target.qubit_properties]) * 1e6
t2 = np.median([q.t2 for q in target.qubit_properties]) * 1e6
print(f"median T1            : {t1:6.1f} us")
print(f"median T2            : {t2:6.1f} us")
for gate in ["sx", "cz", "measure"]:
    e, d = median_error(gate), median_time(gate) * 1e9
    print(f"median {gate:8s} error: {e:.5f}   duration: {d:5.0f} ns")
# How many CZ gates fit inside one T2 time?
n_cz = t2 * 1e-6 / median_time("cz")
print(f"CZ gates per T2      : {n_cz:.0f}")
