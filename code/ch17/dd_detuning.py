"""Does DD protect an idle qubit from slow frequency drift?"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate
from qiskit.quantum_info import Statevector
from qiskit.transpiler import (PassManager,
                               generate_preset_pass_manager)
from qiskit.transpiler.passes import (ALAPScheduleAnalysis, PadDelay,
                                      PadDynamicalDecoupling)
from qiskit_ibm_runtime.fake_provider import FakeFez

qc = QuantumCircuit(3)
qc.h(0)
qc.barrier()
for _ in range(12):                    # qubit 0 idles meanwhile
    qc.cx(1, 2)
    qc.rx(0.4, 1)
qc.barrier()
qc.h(0)                                # ideal result: qubit 0 in |0>

target = FakeFez().target
pm = generate_preset_pass_manager(optimization_level=1,
                                  target=target,
                                  initial_layout=[20, 21, 22],
                                  seed_transpiler=11)
sched = [ALAPScheduleAnalysis(target=target)]
plain = PassManager(sched + [PadDelay(target=target)]).run(
    pm.run(qc))
pad = PadDynamicalDecoupling(target=target,
                             dd_sequence=[XGate()] * 2)
with_dd = PassManager(sched + [pad]).run(pm.run(qc))

def p0_with_drift(circ, freq_hz):
    """Turn every delay on physical qubit 20 into an RZ phase."""
    small = QuantumCircuit(3)
    for inst in circ.data:
        qs = [circ.find_bit(q).index - 20 for q in inst.qubits]
        op = inst.operation
        if op.name == "delay" and qs == [0]:
            phase = 2 * np.pi * freq_hz * op.duration * target.dt
            small.rz(phase, 0)
        elif op.name not in ("delay", "barrier"):
            small.append(op, qs)
    return Statevector(small).probabilities([0])[0]

idle = sum(i.operation.duration for i in plain.data
           if i.operation.name == "delay"
           and plain.find_bit(i.qubits[0]).index == 20)
print(f"qubit 0 waits {idle * target.dt * 1e9:.0f} ns"
      " in superposition")
n_x = sum(1 for i in with_dd.data if i.operation.name == "x")
print(f"X gates inserted by the DD pass: {n_x}")
rng = np.random.default_rng(8)
drifts = rng.normal(0, 150e3, size=100)   # 150 kHz spread
for name, circ in [("no DD", plain), ("XX DD", with_dd)]:
    p = [p0_with_drift(circ, f) for f in drifts]
    print(f"{name}: average P(qubit 0 = 0) = {np.mean(p):.4f}")
