# Superdense coding sends two classical bits with one qubit.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit.transpiler import generate_preset_pass_manager

def superdense(message):               # message "m1 m0", e.g. "10"
    qc = QuantumCircuit(2)             # q0 Alice, q1 Bob
    qc.h(0); qc.cx(0, 1)               # shared Bell pair
    if message[0] == "1":              # Alice encodes on q0 only
        qc.x(0)
    if message[1] == "1":
        qc.z(0)
    qc.cx(0, 1); qc.h(0)               # Bob decodes (Bell basis)
    qc.measure_all()
    return qc

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
noisy = AerSampler.from_backend(
    AerSimulator.from_backend(backend, seed_simulator=1234))
ideal = StatevectorSampler(seed=3)
for msg in ["00", "01", "10", "11"]:
    qc = superdense(msg)
    c1 = ideal.run([qc], shots=1000).result()[0]\
        .data.meas.get_counts()
    c2 = noisy.run([pm.run(qc)], shots=1000).result()[0]\
        .data.meas.get_counts()
    print(f"sent {msg}: ideal {c1}  noisy success "
          f"{c2.get(msg, 0) / 1000:.3f}")
