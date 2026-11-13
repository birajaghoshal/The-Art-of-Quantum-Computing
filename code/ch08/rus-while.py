# Repeat-until-success: prepare (|00>+|01>+|10>)/sqrt(3)
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import (Statevector, DensityMatrix,
                                 state_fidelity)
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

d, a = QuantumRegister(2, "d"), QuantumRegister(1, "anc")
flag, out = ClassicalRegister(1, "flag"), ClassicalRegister(2, "out")

def attempt(qc):
    qc.h(d)                        # uniform over 00, 01, 10, 11
    qc.ccx(d[0], d[1], a[0])       # ancilla = 1 only for 11
    qc.measure(a[0], flag[0])      # herald: 0 means success

qc = QuantumCircuit(d, a, flag, out)
attempt(qc)
with qc.while_loop((flag[0], 1)):  # failed? reset and try again
    qc.reset(d)
    qc.reset(a)
    attempt(qc)

check = qc.copy()                  # version that saves the state
check.save_density_matrix(d, label="rho")
qc.measure(d, out)
fig = qc.draw("mpl", fold=-1, scale=0.75)
fig.savefig("figures/ch08/rus_circuit.pdf", bbox_inches="tight")

sim = AerSimulator(seed_simulator=7)
res = AerSampler.from_backend(sim).run([qc], shots=3000).result()[0]
print("Data counts:",
      dict(sorted(res.data.out.get_counts().items())))
print("Final flags:", res.data.flag.get_counts())

rho = DensityMatrix(sim.run(check, shots=200).result().data()["rho"])
goal = (Statevector.from_label("00") + Statevector.from_label("01")
        + Statevector.from_label("10")) / 3 ** 0.5
print(f"Purity of data qubits: {rho.purity().real:.4f}")
print(f"Fidelity with target: {state_fidelity(rho, goal):.4f}")
