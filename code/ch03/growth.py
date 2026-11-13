"""Polynomial versus exponential step counts, and the time 2**n
steps would take at one billion simple steps per second."""
UNITS = [("seconds", 1), ("minutes", 60), ("hours", 3600),
         ("days", 86400), ("years", 86400 * 365)]

def duration(t):
    """Express t seconds in the largest unit that keeps t >= 1."""
    name, size = max((u for u in UNITS if t >= u[1]),
                     key=lambda u: u[1], default=UNITS[0])
    return f"{t / size:.3g} {name}"

print(f"{'n':>3} {'n^2':>6} {'n^3':>8} {'2^n':>10}  time for 2^n")
for n in (10, 20, 30, 40, 50, 60, 80):
    t = 2.0**n / 1e9                 # seconds at 1e9 steps/second
    print(f"{n:>3} {n**2:>6} {n**3:>8} {2.0**n:>10.3g}  "
          f"{duration(t)}")
