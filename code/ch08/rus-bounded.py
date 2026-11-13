# Bounded repeat-until-success with if_test, on noisy FakeFez
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime.fake_provider import FakeFez

d, a = QuantumRegister(2, "d"), QuantumRegister(1, "anc")
flags = ClassicalRegister(3, "flags")    # one herald per attempt
out = ClassicalRegister(2, "out")
qc = QuantumCircuit(d, a, flags, out)

def attempt(k):
    qc.h(d)
    qc.ccx(d[0], d[1], a[0])
    qc.measure(a[0], flags[k])

attempt(0)
for k in (1, 2):                         # at most two retries
    with qc.if_test((flags[k - 1], 1)):
        qc.reset(d)
        qc.reset(a)
        attempt(k)
qc.measure(d, out)

backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
isa = pm.run(qc)
top = isa.count_ops()
inner = sum(blk.count_ops().get("cz", 0) for inst in isa.data
            if inst.operation.name == "if_else"
            for blk in inst.operation.blocks)
print("Top level: cz =", top["cz"], " if_else =", top["if_else"])
print("CZ gates hidden inside the if_else blocks:", inner)
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
res = AerSampler.from_backend(sim).run([isa], shots=4000).result()[0]
print("Flags (f2 f1 f0):",
      dict(sorted(res.data.flags.get_counts().items())))
print("Data (d1 d0):   ",
      dict(sorted(res.data.out.get_counts().items())))
