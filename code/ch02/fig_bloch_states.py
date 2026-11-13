# Bloch sphere with the six cardinal states and one general state
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10})
fig = plt.figure(figsize=(4.8, 4.6))
ax = fig.add_subplot(projection="3d")
u, w = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
ax.plot_wireframe(np.cos(u) * np.sin(w), np.sin(u) * np.sin(w),
                  np.cos(w), color="0.88", lw=0.5)
t = np.linspace(0, 2 * np.pi, 100)
ax.plot(np.cos(t), np.sin(t), 0 * t, color="0.6", lw=0.8)   # equator

pts = {r"$|0\rangle$": (0, 0, 1), r"$|1\rangle$": (0, 0, -1),
       r"$|+\rangle$": (1, 0, 0), r"$|-\rangle$": (-1, 0, 0),
       r"$|{+i}\rangle$": (0, 1, 0), r"$|{-i}\rangle$": (0, -1, 0)}
cols = ["#1F5FBF", "#1F5FBF", "#0F9D8C", "#0F9D8C", "#F28C28",
        "#F28C28"]
for (lab, p), c in zip(pts.items(), cols):
    ax.plot([0, p[0]], [0, p[1]], [0, p[2]], color=c, lw=1.4)
    ax.scatter(*p, color=c, s=18)
    ax.text(1.18 * p[0], 1.18 * p[1], 1.12 * p[2], lab, color=c,
            ha="center")
th, ph = 2 * np.arccos(0.6), np.pi / 2       # 0.6|0> + 0.8i|1>
q = (np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th))
ax.plot([0, q[0]], [0, q[1]], [0, q[2]], color="#D64545", lw=2.2)
ax.scatter(*q, color="#D64545", s=25)
ax.text(q[0], q[1] - 0.1, q[2] - 0.42,
        r"$0.6|0\rangle+0.8i|1\rangle$", color="#D64545")
ax.set_box_aspect([1, 1, 1], zoom=1.35)
ax.view_init(elev=18, azim=-60)
ax.set_axis_off()
fig.savefig("figures/ch02/bloch_states.pdf", bbox_inches="tight")
print("saved figures/ch02/bloch_states.pdf")
