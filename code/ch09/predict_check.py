# Predict first, then let the simulator check the prediction.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

predicted = {"01": 0.5, "10": 0.5}  # written BEFORE running; "q1 q0"
qc = QuantumCircuit(2)
qc.x(1)        # |10>
qc.h(0)        # (|10> + |11>)/sqrt(2)
qc.cx(0, 1)    # (|10> + |01>)/sqrt(2)

probs = {str(k): round(float(v), 4)
         for k, v in Statevector(qc).probabilities_dict().items()}
keys = set(predicted) | set(probs)
worst = max(abs(predicted.get(k, 0) - probs.get(k, 0)) for k in keys)
print("Simulated:", dict(sorted(probs.items())))
print("Prediction confirmed" if worst < 1e-9 else "MISMATCH")
