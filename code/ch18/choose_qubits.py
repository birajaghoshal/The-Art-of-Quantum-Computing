"""Rank every 6-qubit line on FakeFez by its reported error rates."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

def rank_lines(backend, length=6):
    """All lines of connected qubits, best first, and the scorer."""
    t = backend.target
    cz = {pair: p.error for pair, p in t["cz"].items()}
    ro = {q[0]: p.error for q, p in t["measure"].items()}
    nbrs = {a: {b for x, b in cz if x == a} for a, _ in cz}
    def paths(path):          # depth-first walk along the chip
        if len(path) == length:
            yield path
            return
        for nxt in nbrs[path[-1]] - set(path):
            yield from paths(path + [nxt])
    def score(chain):         # total error budget of a chain
        gates = sum(cz[(a, b)] for a, b in zip(chain, chain[1:]))
        return gates + sum(ro[q] for q in chain)
    # keep one direction per line: a path and its reverse count once
    chains = {tuple(min(p, p[::-1]))
              for q in nbrs for p in paths([q])}
    return sorted(chains, key=score), score

if __name__ == "__main__":
    backend = FakeFez()
    ranked, score = rank_lines(backend)
    print(f"distinct 6-qubit lines : {len(ranked)}")
    print(f"best line  {list(ranked[0])}: "
          f"score {score(ranked[0]):.4f}")
    print(f"median line score      : "
          f"{np.median([score(c) for c in ranked]):.4f}")
    print(f"worst line {list(ranked[-1])}: "
          f"score {score(ranked[-1]):.4f}")
    line = QuantumCircuit(6)  # what does the transpiler pick?
    for q in range(5):
        line.cz(q, q + 1)
    line.measure_all()        # real runs measure, so readout counts
    for level in (1, 2, 3):   # optimisation levels
        pm = generate_preset_pass_manager(level, backend,
                                          seed_transpiler=11)
        lay = pm.run(line).layout
        chosen = lay.initial_index_layout(filter_ancillas=True)
        print(f"level {level} {chosen}: score {score(chosen):.4f}")
