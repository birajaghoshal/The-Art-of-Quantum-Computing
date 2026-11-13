from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def oracle(name):
    """Bit oracle on q0 = x, q1 = y for the four 1-bit functions."""
    qc = QuantumCircuit(2, name=name)
    if name == "f(x)=1":
        qc.x(1)
    elif name == "f(x)=x":
        qc.cx(0, 1)
    elif name == "f(x)=NOT x":
        qc.cx(0, 1)
        qc.x(1)
    return qc                            # "f(x)=0" does nothing

def deutsch(name):
    qc = QuantumCircuit(2, 1)
    qc.x(1)
    qc.h([0, 1])
    qc.compose(oracle(name), inplace=True)
    qc.h(0)
    qc.measure(0, 0)                     # only the input qubit
    return qc

names = ["f(x)=0", "f(x)=1", "f(x)=x", "f(x)=NOT x"]
sampler = StatevectorSampler(seed=10)
for name in names:
    res = sampler.run([deutsch(name)], shots=500).result()
    counts = res[0].data.c.get_counts()
    verdict = "constant" if counts.get("0", 0) == 500 else "balanced"
    print(f"{name:<11} counts = {counts}  ->  {verdict}")
