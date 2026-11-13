# Mutation testing: which tests notice which injected bugs?
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Operator, Statevector
from qtest import exact_probs, sample_counts, fits

def program(theta=1.0, mutant=None):
    qc = QuantumCircuit(2)
    qc.ry(theta / 2 if mutant == "half angle" else theta, 0)
    qc.cx(*((1, 0) if mutant == "swapped cx" else (0, 1)))
    if mutant == "S to Sdg":
        qc.sdg(1)
    elif mutant == "wrong qubit":
        qc.s(0)
    elif mutant != "missing S":
        qc.s(1)
    return qc

ref = program()
sampler = StatevectorSampler(seed=np.random.default_rng(42))
def stat_test(b):
    return lambda qc: fits(sample_counts(qc, b, sampler, 4000),
                           exact_probs(ref, b))
tests = {"ZZ": stat_test("ZZ"), "XX": stat_test("XX"),
         "XY": stat_test("XY"),
         "state": lambda qc: Statevector(qc).equiv(Statevector(ref)),
         "unitary": lambda qc: Operator(qc).equiv(Operator(ref))}
print(f"{'mutant':<12}" + "".join(f"{t:>8}" for t in tests))
for m in [None, "swapped cx", "half angle", "missing S", "S to Sdg",
          "wrong qubit"]:
    row = ["pass" if t(program(mutant=m)) else "KILL"
           for t in tests.values()]
    print(f"{m or 'original':<12}" + "".join(f"{r:>8}" for r in row))
