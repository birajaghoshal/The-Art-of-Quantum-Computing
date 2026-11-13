"""A reversible half adder: one Toffoli and one CNOT.
Qubits: q0 = a, q1 = b, q2 = carry (starts at 0)."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(3)
qc.ccx(0, 1, 2)      # carry ^= a AND b
qc.cx(0, 1)          # b becomes a XOR b, the sum bit
print("a b -> a sum carry")
for a in (0, 1):
    for b in (0, 1):
        # Labels read q2 q1 q0, so carry = bits[0] and a = bits[2]
        label = f"0{b}{a}"
        out = Statevector.from_label(label).evolve(qc)
        probs = out.probabilities_dict()
        bits = max(probs, key=probs.get)   # the one certain outcome
        carry, s, a_out = bits[0], bits[1], bits[2]
        print(f"{a} {b} ->  {a_out}   {s}    {carry}")
