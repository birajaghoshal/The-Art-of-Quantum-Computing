# Entanglement entropy of one qubit with the rest of the register
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, entropy

product = QuantumCircuit(3)
product.h([0, 1, 2])             # |+++>, no entanglement

bell = QuantumCircuit(3)
bell.h(0); bell.cx(0, 1)         # Bell pair on q0,q1; q2 idle

ghz = QuantumCircuit(3)
ghz.h(0); ghz.cx(0, 1); ghz.cx(1, 2)

w = Statevector.from_label("001") + Statevector.from_label("010") \
    + Statevector.from_label("100")
w = w / 3 ** 0.5                 # the W state

states = {"|+++>": Statevector(product),
          "Bell+|0>": Statevector(bell),
          "GHZ": Statevector(ghz), "W": w}
print(f"{'state':9s}  S(q0)   S(q2)")
for name, psi in states.items():
    s0 = entropy(partial_trace(psi, [1, 2]), base=2)   # keep q0
    s2 = entropy(partial_trace(psi, [0, 1]), base=2)   # keep q2
    print(f"{name:9s}  {s0:.3f}   {s2:.3f}")

print("Reduced state of q0 in GHZ:")
print(partial_trace(states["GHZ"], [1, 2]).data.real.round(3))
