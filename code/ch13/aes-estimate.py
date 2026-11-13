# Back-of-envelope: Grover key search against AES
import numpy as np

SECONDS_PER_YEAR = 3.156e7
t_iter = 1e-6   # ASSUMED time per Grover iteration (very optimistic)
print(f"assumed time per iteration: {t_iter:.0e} s")
print(f"{'key bits':>8} {'iterations':>11} {'1 machine':>15}"
      f" {'1e6 machines':>15}")
for bits in (128, 192, 256):
    iters = np.pi / 4 * 2 ** (bits / 2)
    years_one = iters * t_iter / SECONDS_PER_YEAR
    # P machines split the key space: each needs sqrt(2^bits / P)
    years_par = years_one / np.sqrt(1e6)
    print(f"{bits:>8} {iters:>11.2e} {years_one:>11.2e} yrs"
          f" {years_par:>11.2e} yrs")
