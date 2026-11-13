# Figure: one Grover iteration as two reflections in a plane
import numpy as np
import matplotlib.pyplot as plt

half = np.arcsin(np.sqrt(1 / 16))      # theta/2 for N = 16, M = 1
fig, ax = plt.subplots(figsize=(4.8, 3.14))
ax.set_aspect("equal")
t = np.linspace(0, np.pi / 2, 100)
ax.plot(np.cos(t), np.sin(t), color="#BBBBBB", lw=0.8)

def arrow(angle, colour, label, dx=0.04, dy=0.0):
    x, y = np.cos(angle), np.sin(angle)
    ax.annotate("", (x, y), (0, 0), arrowprops=dict(
        arrowstyle="-|>", color=colour, lw=1.6))
    ax.text(x + dx, y + dy, label, color=colour, fontsize=14)

ax.annotate("", (1.12, 0), (0, 0), arrowprops=dict(arrowstyle="-|>",
            color="black", lw=0.8))
ax.annotate("", (0, 1.12), (0, 0), arrowprops=dict(arrowstyle="-|>",
            color="black", lw=0.8))
ax.text(1.14, -0.04, r"$|\beta\rangle$ (unmarked)", fontsize=14)
ax.text(-0.05, 1.15, r"$|\alpha\rangle$ (marked)", fontsize=14)
arrow(half, "#1F5FBF", r"$|s\rangle$")
arrow(-half, "#F28C28", r"$O|s\rangle$", dy=-0.08)
arrow(3 * half, "#0F9D8C", r"$G|s\rangle$")
arrow(5 * half, "#7B4FBF", r"$G^2|s\rangle$", dy=0.03)
for a1, a2, r, lab in [(0, half, 0.8, r"$\theta/2$"),
                       (half, 3 * half, 0.5, r"$\theta$")]:
    tt = np.linspace(a1, a2, 30)
    ax.plot(r * np.cos(tt), r * np.sin(tt), color="#555555", lw=0.8)
    m = (a1 + a2) / 2
    ax.text((r + 0.04) * np.cos(m), (r + 0.04) * np.sin(m), lab,
            fontsize=14, va="center")
ax.set_xlim(-0.15, 1.6)
ax.set_ylim(-0.45, 1.25)
ax.axis("off")
fig.tight_layout()
fig.savefig("figures/ch13/geometry.pdf")
print("saved figures/ch13/geometry.pdf")
