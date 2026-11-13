# Factoring N = 91 by finding the order of a (classically, slowly)
from math import gcd

def order(a, N):
    """Smallest r > 0 with a^r = 1 (mod N), by brute force."""
    r, y = 1, a % N
    while y != 1:
        y = (y * a) % N
        r += 1
    return r

N = 91

# How often does a random a work for N = 91?
tally = {"lucky gcd": 0, "odd r": 0, "a^(r/2) = -1": 0, "success": 0}
for a in range(2, N):
    if gcd(a, N) > 1:
        tally["lucky gcd"] += 1
        continue
    r = order(a, N)
    if r % 2 == 1:
        tally["odd r"] += 1
    elif pow(a, r // 2, N) == N - 1:
        tally["a^(r/2) = -1"] += 1
    else:
        tally["success"] += 1
print(f"outcomes for a = 2..{N - 1}:")
print(tally)
