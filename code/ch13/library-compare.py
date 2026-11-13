# Our hand-built Grover iteration versus qiskit's grover_operator
from qiskit import transpile
from qiskit.circuit.library import grover_operator
from qiskit.quantum_info import Operator
from groverlib import phase_oracle, diffuser

n, marked = 4, ["1011"]
oracle = phase_oracle(n, marked)
mine = oracle.compose(diffuser(n))      # oracle, then diffuser
lib = grover_operator(oracle)
print("same up to global phase:",
      Operator(mine).equiv(Operator(lib)))

basis = ["cx", "rz", "sx", "x"]
for name, qc in [("hand-built", mine), ("grover_operator", lib)]:
    t = transpile(qc, basis_gates=basis, optimization_level=1,
                  seed_transpiler=1)
    print(f"{name:>16}: depth {t.depth():>3}, "
          f"CNOTs {t.count_ops().get('cx', 0)}")
