# What X, Y and Z do to |0>, |1> and |+>: states and Bloch vectors.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

def c2s(z):
    a, b = round(z.real, 3) + 0, round(z.imag, 3) + 0
    if b == 0:
        return f"{a:g}"
    s = {1: "", -1: "-"}.get(b, f"{b:g}") + "i"
    return s if a == 0 else f"{a:g}{'+' if b > 0 else ''}{s}"

def bloch(psi):
    """Bloch vector (<X>, <Y>, <Z>) of a one-qubit state."""
    ev = [psi.expectation_value(SparsePauliOp(p)).real
          for p in "XYZ"]
    return "(" + ", ".join(f"{round(v):2d}" for v in ev) + ")"

for start in ["0", "1", "+"]:
    psi = Statevector.from_label(start)
    print(f"{'|' + start + '>':27s} Bloch {bloch(psi)}")
    for gate in ["x", "y", "z"]:
        qc = QuantumCircuit(1)
        getattr(qc, gate)(0)              # qc.x(0), qc.y(0), qc.z(0)
        out = psi.evolve(qc)
        amps = "(" + ", ".join(c2s(z) for z in out.data) + ")"
        line = f"{gate.upper()}|{start}> = {amps}"
        print(f"  {line:25s} Bloch {bloch(out)}")
