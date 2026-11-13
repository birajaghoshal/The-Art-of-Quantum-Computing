# BB84: sifting and the quantum bit error rate (QBER).
import numpy as np
from bb84_sim import run_bb84

r = run_bb84(16, seed=4)               # a short run, shown in full
sym = lambda basis: "".join("+x"[b] for b in basis)
keep = r["a_basis"] == r["b_basis"]
print("Alice bits   ", "".join(map(str, r["a_bit"])))
print("Alice bases  ", sym(r["a_basis"]))
print("Bob bases    ", sym(r["b_basis"]))
print("Bob bits     ", "".join(map(str, r["b_bit"])))
print("Sifted key   ", "".join(str(b) if k else "." for b, k
                               in zip(r["b_bit"], keep)))

for eve in (0.0, 1.0):
    r = run_bb84(2000, eve=eve, seed=7)
    keep = r["a_basis"] == r["b_basis"]
    errors = np.sum(r["a_bit"][keep] != r["b_bit"][keep])
    eve_ok = np.mean(r["e_bit"][keep] == r["a_bit"][keep])
    print(f"Eve={'on ' if eve else 'off'}: sifted {keep.sum()} of"
          f" 2000, errors {errors}, QBER {errors / keep.sum():.3f}")
    if eve:
        print(f"         Eve's copy agrees with Alice on "
              f"{eve_ok:.3f} of the sifted bits")
