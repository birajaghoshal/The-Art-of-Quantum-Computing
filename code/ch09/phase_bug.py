# Phase bugs are invisible in the Z basis. Change basis to see them.
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qtest import sample_counts

sampler = StatevectorSampler(seed=np.random.default_rng(5))
singlet = QuantumCircuit(2)                   # (|01> - |10>)/sqrt 2
singlet.x(1); singlet.h(0); singlet.z(0); singlet.cx(0, 1)
buggy = QuantumCircuit(2)                     # forgot the Z: Psi+
buggy.x(1); buggy.h(0); buggy.cx(0, 1)
for basis in ("ZZ", "XX"):
    for name, qc in [("singlet", singlet), ("buggy", buggy)]:
        print(f"{basis} {name:<7}:", sample_counts(qc, basis,
                                                   sampler, 1000))
plus_i = QuantumCircuit(1); plus_i.h(0); plus_i.s(0)
wrong = QuantumCircuit(1); wrong.h(0); wrong.sdg(0)
for basis in ("Z", "X", "Y"):
    s_counts = sample_counts(plus_i, basis, sampler, 1000)
    sdg_counts = sample_counts(wrong, basis, sampler, 1000)
    print(f"{basis}  S  :", s_counts, "  Sdg:", sdg_counts)
