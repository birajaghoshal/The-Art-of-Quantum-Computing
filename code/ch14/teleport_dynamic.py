# Teleportation with mid-circuit measurement and feed-forward.
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

theta, phi = 1.1, 0.7                  # the state Alice will send

def teleport():
    q = QuantumRegister(3, "q")        # q0 message, q1 Alice, q2 Bob
    m = ClassicalRegister(2, "m")      # Alice's two results
    qc = QuantumCircuit(q, m)
    qc.ry(theta, 0); qc.rz(phi, 0)     # prepare |psi> on q0
    qc.h(1); qc.cx(1, 2)               # share a Bell pair
    qc.barrier()
    qc.cx(0, 1); qc.h(0)               # Alice's Bell measurement
    qc.measure(0, m[0]); qc.measure(1, m[1])
    with qc.if_test((m[1], 1)):        # Bob's corrections
        qc.x(2)
    with qc.if_test((m[0], 1)):
        qc.z(2)
    return qc

if __name__ == "__main__":
    qc = teleport()
    check = ClassicalRegister(1, "bob")
    qc.add_register(check)
    qc.rz(-phi, 2); qc.ry(-theta, 2)   # undo the preparation...
    qc.measure(2, check[0])            # ...so Bob should read 0
    sampler = AerSampler.from_backend(
        AerSimulator(seed_simulator=21))
    data = sampler.run([qc], shots=2000).result()[0].data
    print("Alice's results:",
          dict(sorted(data.m.get_counts().items())))
    print("Bob's check    :", data.bob.get_counts())
