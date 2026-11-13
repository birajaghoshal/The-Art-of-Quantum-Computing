from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def show(label, qc):
    """Print nonzero amplitudes; labels read |q1 q0> = |y x>."""
    sv = Statevector(qc)
    terms = [f"{a.real:+.3f}|{k}>" for k, a in
             sv.to_dict().items() if abs(a) > 1e-9]
    print(f"{label:<16}", "  ".join(terms))

qc = QuantumCircuit(2)                  # q0 = x (input), q1 = y
qc.x(1)
show("start |1>|0>", qc)
qc.h([0, 1])
show("after H, H", qc)
qc.cx(0, 1)                             # oracle for f(x) = NOT x:
qc.x(1)                                 # y -> y XOR x XOR 1
show("after oracle", qc)
qc.h(0)
show("after final H", qc)
