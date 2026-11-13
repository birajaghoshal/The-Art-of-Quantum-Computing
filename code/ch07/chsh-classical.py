# Best classical CHSH score: try every deterministic strategy
from itertools import product

best, count = -10, 0
# Alice answers a0, a1 (for settings 0, 1); Bob answers b0, b1
for a0, a1, b0, b1 in product([+1, -1], repeat=4):
    s = a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1
    count += 1
    best = max(best, s)
    if s == 2 and (a0, a1) == (1, 1):
        print(f"winning example: a = ({a0},{a1}), b = ({b0},{b1})")
print(f"strategies tried: {count}, largest S: {best}")
print("Win probability of the best strategy:", (best + 4) / 8)
