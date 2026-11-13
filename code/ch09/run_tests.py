# Run the pytest suite from Python, then once per injected mutant.
import io, os
from contextlib import redirect_stdout
import pytest

class Collector:                  # a tiny plugin: records outcomes
    def __init__(self):
        self.results = {}
    def pytest_runtest_logreport(self, report):
        if report.when == "call" or report.outcome == "failed":
            self.results[report.nodeid.split("::")[-1]] = \
                report.outcome

def run_suite(mutant=""):
    os.environ["CH09_MUTANT"] = mutant
    col = Collector()
    args = ["-q", "-p", "no:cacheprovider",
            "code/ch09/test_circuits.py"]
    with redirect_stdout(io.StringIO()):      # hide timing lines
        code = pytest.main(args, plugins=[col])
    return int(code), col.results

for m in ["", "reversed bits", "missing cx", "phase flip"]:
    code, res = run_suite(m)
    bad = [n for n, o in res.items() if o == "failed"]
    print(f"{m or 'original':<14} exit={code}  passed="
          f"{len(res) - len(bad)}  failed={len(bad)}")
    for name in bad:
        print("     failed:", name)
