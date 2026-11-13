# Plot <X> and purity of a dephased |+> state against error rate p
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 11})
p = np.linspace(0, 0.5, 101)
x = 1 - 2 * p                            # Bloch x component
purity = (1 + x ** 2) / 2

fig, ax = plt.subplots(figsize=(5, 2.8))
ax.plot(p, x, color="#1F5FBF", label=r"$\langle X\rangle = 1-2p$")
ax.plot(p, purity, color="#F28C28",
        label=r"purity $\mathrm{Tr}(\rho^2)$")
ax.axhline(0.5, color="0.7", ls=":", lw=1)
arrow = dict(arrowstyle="->", color="0.3", lw=0.9)
for target in [(0.5, 0.5), (0.5, 0.0)]:
    ax.annotate("fully mixed\nat p = 0.5", xy=target, xytext=(0.355, 0.78),
                fontsize=10, ha="center", arrowprops=arrow)
ax.set_xlabel("probability p of a Z error")
ax.set_ylabel("value")
ax.set_ylim(-0.05, 1.05)
ax.set_xlim(0, 0.52)
ax.grid(color="0.92")
ax.legend(loc="lower left", fontsize=10)
fig.tight_layout()
fig.savefig("figures/ch02/dephasing.pdf", bbox_inches="tight")
print("saved figures/ch02/dephasing.pdf")
