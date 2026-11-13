# Order finding for a = 2, N = 21 with 10 counting qubits
from fractions import Fraction
import matplotlib.pyplot as plt
from qiskit.primitives import StatevectorSampler
from shorlib import order_finding, guess_order, factors_from_order

a, N, t = 2, 21, 10
qc = order_finding(a, N, t)
print("qubits:", qc.num_qubits)
sampler = StatevectorSampler(seed=21)
counts = sampler.run([qc], shots=2000).result()[0].data.c \
    .get_counts()

top = sorted(counts.items(), key=lambda kv: -kv[1])[:8]
for bits, c in sorted(top, key=lambda kv: int(kv[0], 2)):
    k = int(bits, 2)
    frac = Fraction(k, 2**t).limit_denominator(N)
    print(f"k = {k:>4} ({c:>3} shots): {k / 2**t:.4f} -> "
          f"{str(frac):>3}, r = {guess_order(k, t, a, N)}")

good = sum(c for b, c in counts.items()
           if factors_from_order(a, guess_order(int(b, 2), t, a, N),
                                 N))
print(f"distinct outcomes: {len(counts)}, "
      f"shots giving a factor: {good}/2000")
print("factors:", factors_from_order(a, 6, N))

fig, ax = plt.subplots(figsize=(4.6, 2.15))
ks = sorted(int(b, 2) for b in counts)
ax.bar([k / 2**t for k in ks],
       [counts[format(k, "010b")] for k in ks],
       width=0.006, color="#0F9D8C")
for s in range(6):
    ax.axvline(s / 6, color="#A04A00", ls=":", lw=1.2, zorder=3)
ax.set(yscale="log", ylim=(0.5, 600))  # shows the small neighbours
ax.set_xlabel("measured phase  k / 1024   (dotted lines: s/6)")
ax.set_ylabel("shots (of 2000)")
fig.tight_layout()
fig.savefig("figures/ch12/shor21_hist.pdf")
