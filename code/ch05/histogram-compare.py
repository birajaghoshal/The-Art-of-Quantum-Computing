# Ideal and noisy counts side by side with plot_histogram.
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.transpiler import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

qc = QuantumCircuit(2)
qc.h(0)                  # q0: fair coin
qc.x(1)                  # q1: always 1
qc.measure_all()

ideal = StatevectorSampler(seed=4).run([qc], shots=2000).result()
backend = FakeFez()
pm = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=11)
sim = AerSimulator.from_backend(backend, seed_simulator=1234)
noisy = AerSampler.from_backend(sim).run([pm.run(qc)],
                                         shots=2000).result()
c_ideal = ideal[0].data.meas.get_counts()
c_noisy = noisy[0].data.meas.get_counts()
print("ideal:", dict(sorted(c_ideal.items())))
print("noisy:", dict(sorted(c_noisy.items())))

fig = plot_histogram([c_ideal, c_noisy], legend=["ideal", "FakeFez"],
                     color=["#1F5FBF", "#F28C28"], figsize=(6, 3.6))
fig.axes[0].set_ylim(0, 1150)
fig.savefig("figures/ch05/histogram-compare.pdf",
            bbox_inches="tight")
print("saved figures/ch05/histogram-compare.pdf")
