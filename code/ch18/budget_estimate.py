"""Rough QPU-time floor for a planned experiment on Heron devices."""
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

backend = FakeFez()
rep_delay = backend.configuration().default_rep_delay  # seconds
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)

def ghz(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    for q in range(n - 1):
        qc.cx(q, q + 1)
    qc.measure_all()
    return qc

print(f"default repetition delay: {rep_delay * 1e6:.0f} us")
budget = 10 * 60                                       # Open Plan, s
plans = [(6, 1, 4000), (6, 30, 4000), (20, 100, 8000)]
for n, n_circ, shots in plans:
    isa = pm.run(ghz(n))
    t_circ = isa.estimate_duration(backend.target, unit="s")
    floor = n_circ * shots * (t_circ + rep_delay)
    print(f"{n:2d} qubits, {n_circ:3d} circuit(s) x {shots}: "
          f"{t_circ*1e6:.2f} us, floor {floor:5.1f} s "
          f"({100 * floor / budget:4.1f}%)")
