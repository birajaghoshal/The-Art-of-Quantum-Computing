# How precisely do N shots estimate a probability p?
import numpy as np

p = 0.3                                 # true probability of "1"
rng = np.random.default_rng(seed=11)
print("   N   predicted SE   measured SE   one estimate")
for N in [100, 1000, 10000]:
    # 5000 repeated experiments, each with N shots
    ones = rng.binomial(N, p, size=5000)
    estimates = ones / N
    se_theory = np.sqrt(p * (1 - p) / N)
    print(f"{N:6d}   {se_theory:.4f}         {estimates.std():.4f}"
          f"        {estimates[0]:.4f}")
# Shots needed for a standard error of 0.01 when p is near 0.5
print("shots for SE = 0.01 at p = 0.5:", int(0.25 / 0.01**2))
