"""Compute a AND b AND c with a helper (ancilla) qubit, then
uncompute the helper so it returns to 0.
Qubits: q0=a, q1=b, q2=c, q3=helper, q4=output."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def and3(clean_up):
    qc = QuantumCircuit(5)
    qc.ccx(0, 1, 3)          # helper = a AND b
    qc.ccx(2, 3, 4)          # output ^= c AND helper
    if clean_up:
        qc.ccx(0, 1, 3)      # undo step 1: helper back to 0
    return qc

def run(qc, label):
    out = Statevector.from_label(label).evolve(qc)
    probs = out.probabilities_dict()
    return max(probs, key=probs.get)   # the one certain outcome

print("        without uncompute   with uncompute")
print("a b c    helper  out        helper  out")
for x in range(8):
    a, b, c = x & 1, (x >> 1) & 1, (x >> 2) & 1
    label = f"00{c}{b}{a}"           # order q4 q3 q2 q1 q0
    dirty, clean = run(and3(False), label), run(and3(True), label)
    print(f"{a} {b} {c}      {dirty[1]}      {dirty[0]}"
          f"           {clean[1]}      {clean[0]}")
