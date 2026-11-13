"""pytest tests for circuits_under_test.py (run via run_tests.py)."""
import pytest
from qiskit.circuit.library import SwapGate
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Operator, Statevector
from circuits_under_test import encode_bits, swap_from_cx, ghz
from qtest import exact_probs, sample_counts, fits

@pytest.mark.parametrize("bits", ["001", "100", "110"])
def test_encode_bits(bits):
    want = Statevector.from_label(bits)
    assert Statevector(encode_bits(bits)).equiv(want)

def test_swap():
    assert Operator(swap_from_cx()).equiv(Operator(SwapGate()))

def test_ghz_counts():
    sampler = StatevectorSampler(seed=123)    # fixed: deterministic
    counts = sample_counts(ghz(3), "ZZZ", sampler, 2000)
    assert fits(counts, {"000": 0.5, "111": 0.5})

def test_ghz_x_parity():
    probs = exact_probs(ghz(3), "XXX")
    odd = sum(p for k, p in probs.items() if k.count("1") % 2)
    assert odd == pytest.approx(0.0, abs=1e-9)
