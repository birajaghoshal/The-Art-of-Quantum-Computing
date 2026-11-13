# Draw a unit sphere with one point and its angles theta and phi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

plt.rcParams.update({"font.size": 11})
fig = plt.figure(figsize=(4.6, 3.9))
ax = fig.add_subplot(projection="3d")
u, w = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
ax.plot_wireframe(np.cos(u) * np.sin(w), np.sin(u) * np.sin(w),
                  np.cos(w), color="0.55", lw=0.5, alpha=0.25)
for d in np.eye(3):
    ax.plot(*zip(-d, 1.3 * d), color="0.55", lw=0.8)
ax.text(1.38, 0, 0, "x")
ax.text(0, 1.38, 0, "y")
ax.text(0, 0, 1.36, "z")

th, ph = np.deg2rad(55), np.deg2rad(40)
p = [np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
ax.plot([0, p[0]], [0, p[1]], [0, p[2]], color="#7B4FBF", lw=2)
ax.scatter(*p, color="#7B4FBF", s=25)
ax.plot([0, p[0]], [0, p[1]], [0, 0], color="#0F9D8C", ls="--")
ax.plot([p[0], p[0]], [p[1], p[1]], [0, p[2]], color="#0F9D8C",
        ls=":")
s = np.linspace(0, th, 30)                    # arc for theta
ax.plot(0.35 * np.sin(s) * np.cos(ph), 0.35 * np.sin(s) * np.sin(ph),
        0.35 * np.cos(s), color="#F28C28", lw=1.8)
ax.text(0.15, 0.1, 0.45, r"$\theta$", color="#F28C28", fontsize=13)
s = np.linspace(0, ph, 30)                    # arc for phi
ax.plot(0.4 * np.cos(s), 0.4 * np.sin(s), 0 * s, color="#D64545",
        lw=1.8)
ax.text(0.62, 0.12, -0.2, r"$\phi$", color="#D64545", fontsize=13)
ax.text(p[0] + 0.05, p[1], p[2] + 0.08, "P", color="#7B4FBF")
ax.set_box_aspect([1, 1, 1], zoom=1.4)
ax.view_init(elev=20, azim=-30)
ax.set_axis_off()
# Crop to the drawn ink: a 3D axes box is square and leaves white margins
fig.canvas.draw()
img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
rows, cols = np.nonzero((img < 250).any(axis=2))
h = img.shape[0]
box = Bbox([[cols.min(), h - rows.max()], [cols.max(), h - rows.min()]])
box = box.transformed(fig.dpi_scale_trans.inverted()).padded(0.04)
fig.savefig("figures/ch01/sphere.pdf", bbox_inches=box)
print("saved figures/ch01/sphere.pdf")
