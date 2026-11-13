"""Three-qubit bit-flip code with a mid-circuit syndrome."""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

def bitflip_circuit(error_on=None):
    data, anc = QuantumRegister(3, "d"), QuantumRegister(2, "a")
    syn = ClassicalRegister(2, "syn")
    out = ClassicalRegister(3, "out")
    qc = QuantumCircuit(data, anc, syn, out)
    qc.x(data[0])                       # logical |1>: start from |1>
    qc.cx(data[0], data[1])             # encode |1> -> |111>
    qc.cx(data[0], data[2])
    qc.barrier()
    if error_on is not None:
        qc.x(data[error_on])            # deliberate error
    qc.barrier()
    qc.cx(data[0], anc[0])              # a0 = d0 xor d1
    qc.cx(data[1], anc[0])
    qc.cx(data[1], anc[1])              # a1 = d1 xor d2
    qc.cx(data[2], anc[1])
    qc.measure(anc, syn)                # mid-circuit measurement
    for value, target in [(1, 0), (3, 1), (2, 2)]:
        with qc.if_test((syn, value)):  # syn read as integer a1 a0
            qc.x(data[target])
    qc.measure(data, out)
    return qc

sampler = AerSampler.from_backend(AerSimulator(seed_simulator=3))
for err in [None, 0, 1, 2]:
    res = sampler.run([bitflip_circuit(err)], shots=100).result()[0]
    syn = res.data.syn.get_counts()
    out = res.data.out.get_counts()
    label = "no error " if err is None else f"X on d{err}  "
    print(f"{label}: syndrome {syn}  data {out}")
