# Several marked items: n = 4 with M = 1, 2, 3, 4 solutions
from qiskit.primitives import StatevectorSampler
from groverlib import grover_circuit, best_k, theory

N = 16
print(f"{'M':>2} {'best k':>7} " +
      " ".join(f"{'k=' + str(k):>6}" for k in range(5)))
for M in (1, 2, 3, 4):
    probs = " ".join(f"{theory(N, M, k):6.3f}" for k in range(5))
    print(f"{M:>2} {best_k(N, M):>7} {probs}")

marked = ["0011", "0110", "1100"]          # M = 3
qc = grover_circuit(4, marked, k=1)
sampler = StatevectorSampler(seed=3)
counts = sampler.run([qc], shots=1000).result()[0].data.meas \
    .get_counts()
hits = {s: counts.get(s, 0) for s in marked}
print("M = 3, k = 1:", hits, "total", sum(hits.values()), "/ 1000")
