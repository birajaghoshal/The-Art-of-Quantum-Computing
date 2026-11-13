# Spread of probability estimates versus number of shots (log-log)
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10})
p = 0.3
rng = np.random.default_rng(seed=3)
Ns = np.unique(np.logspace(1, 4.5, 15).astype(int))
spread = [(rng.binomial(N, p, size=5000) / N).std() for N in Ns]

fig, ax = plt.subplots(figsize=(4.6, 2.5))
ax.loglog(Ns, np.sqrt(p * (1 - p) / Ns), color="#1F5FBF",
          label=r"theory $\sqrt{p(1-p)/N}$")
ax.loglog(Ns, spread, "o", color="#F28C28", ms=5,
          label="measured spread (5000 repeats)")
ax.set_xlabel("number of shots N")
ax.set_ylabel("standard error")
ax.grid(True, which="major", color="0.9")
ax.set_ylim(4e-4, 0.25)
ax.legend(loc="lower left", fontsize=9)
fig.tight_layout()
fig.savefig("figures/ch01/shots.pdf", bbox_inches="tight")
print("saved figures/ch01/shots.pdf")
