# Let the transpiler merge a long run of single-qubit gates.
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.transpiler import generate_preset_pass_manager

qc = QuantumCircuit(1)
qc.h(0)
qc.t(0)
qc.h(0)
qc.h(0)              # H H = I: should vanish
qc.tdg(0)            # cancels the T
qc.s(0)
qc.x(0)
qc.rz(pi / 3, 0)
qc.y(0)
qc.sdg(0)
names = " ".join(inst.operation.name for inst in qc.data)
print("original:", qc.size(), "gates:", names)

pm = generate_preset_pass_manager(optimization_level=1,
                                  basis_gates=["rz", "sx", "x"])
short = pm.run(qc)
names = " ".join(inst.operation.name for inst in short.data)
print("after:   ", short.size(), "gates:", names)
print("equivalent:", Operator(short).equiv(Operator(qc)))
print(short.draw("text", fold=68))
