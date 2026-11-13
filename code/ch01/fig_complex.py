# Two panels: rotation by e^{i theta}, and the 8th roots of unity
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.4, 3.3))
t = np.linspace(0, 2 * np.pi, 300)

z = 2 + 1j
uz = np.exp(1j * np.pi / 3) * z
for ax in (ax1, ax2):
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(0, color="0.6", lw=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel("Re")
    ax.set_ylabel("Im")

ax1.plot(abs(z) * np.cos(t), abs(z) * np.sin(t), color="0.85")
for c, lab, col in [(z, "$z$", "#1F5FBF"),
                    (uz, r"$e^{i\pi/3}z$", "#7B4FBF"),
                    (np.conj(z), r"$\bar z$", "#0F9D8C")]:
    ax1.annotate("", xy=(c.real, c.imag), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6))
    ax1.text(c.real + 0.1, c.imag + 0.1, lab, color=col)
ax1.set_xlim(-2.0, 2.9)
ax1.set_ylim(-2.4, 2.6)
ax1.set_title("Multiplying by $e^{i\\theta}$ rotates")

ax2.plot(np.cos(t), np.sin(t), color="#1F5FBF", lw=1.2)
roots = np.exp(2j * np.pi * np.arange(8) / 8)
ax2.plot(roots.real, roots.imag, "o", color="#F28C28")
for k, r in enumerate(roots):
    ax2.text(1.2 * r.real - 0.12, 1.2 * r.imag - 0.07,
             rf"$\omega^{k}$", fontsize=9)
ax2.set_xlim(-1.45, 1.45)
ax2.set_ylim(-1.45, 1.45)
ax2.set_title(r"8th roots of unity, $\omega=e^{2\pi i/8}$")
fig.tight_layout()
fig.savefig("figures/ch01/complex_plane.pdf", bbox_inches="tight")
print("saved figures/ch01/complex_plane.pdf")
