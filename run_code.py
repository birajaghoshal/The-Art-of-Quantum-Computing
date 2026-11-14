"""Run every example script and capture its output next to it.

Usage (from the project root):
    python3 tools/run_code.py            # all chapters
    python3 tools/run_code.py ch05 ch06  # selected chapters
    python3 tools/run_code.py code/ch05/bell.py   # one script

Each code/chNN/name.py is executed with the project root as the working
directory. Its standard output is written to code/chNN/name.txt, which the
book typesets with \\pyoutput. Scripts whose first line contains
"# norun" need an IBM Quantum account and are skipped.
A non-zero exit code is reported as a failure.
"""
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
TIMEOUT = 600


def targets(args):
    if not args:
        return sorted((ROOT / "code").glob("ch*/*.py"))
    out = []
    for a in args:
        p = ROOT / a
        if p.suffix == ".py":
            out.append(p)
        else:
            out.extend(sorted((ROOT / "code" / a).glob("*.py")))
    return out


def main():
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONHASHSEED="0",
               PYTHONWARNINGS="ignore")
    failures = []
    for script in targets(sys.argv[1:]):
        first = script.read_text(encoding="utf8").splitlines()[:1]
        if first and "norun" in first[0]:
            print(f"SKIP  {script.relative_to(ROOT)} (needs IBM account)")
            continue
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, str(script)], cwd=ROOT,
                               env=env, capture_output=True, text=True,
                               timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            failures.append(script)
            print(f"TIME  {script.relative_to(ROOT)}")
            continue
        script.with_suffix(".txt").write_text(r.stdout.rstrip() + "\n",
                                              encoding="utf8")
        status = "OK  " if r.returncode == 0 else "FAIL"
        print(f"{status}  {script.relative_to(ROOT)}  ({time.time()-t0:.1f}s)")
        if r.returncode != 0:
            failures.append(script)
            print(r.stderr[-2000:])
    if failures:
        print(f"\n{len(failures)} failing script(s)")
        sys.exit(1)
    print("\nAll scripts passed.")


if __name__ == "__main__":
    main()
