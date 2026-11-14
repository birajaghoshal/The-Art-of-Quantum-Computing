# The Art of Quantum Computing: companion code

Companion code for *The Art of Quantum Computing: Fundamentals, Algorithms and Applications using Qiskit* by Dr. Biraja Ghoshal (First Edition, 2026).

Every listing in the book is a short, self-contained script in the `code/` folder, organised by chapter, with one file per listing. Appendix A of the book describes the setup below in full.

## Contents

```
requirements.txt     pinned package versions used to build the book
code/ch01/ ... ch18/ one script per listing (name.py) and its saved output (name.txt)
tools/run_code.py    runs the scripts of one chapter, or all of them, and captures their output
figures/ch01/ ...    where the plotting scripts write their figures
```

Run every command below from this top-level folder, not from inside `code/`.

## 1. Install Python and create a virtual environment

Install Python 3.11 or newer (the book was built with Python 3.13) from <https://www.python.org> or your operating system's package manager. Then create an isolated environment for the book:

```bash
# macOS or Linux
python3 -m venv qiskit-book
source qiskit-book/bin/activate

# Windows (PowerShell)
py -m venv qiskit-book
qiskit-book\Scripts\Activate.ps1
```

## 2. Install the pinned packages

`requirements.txt` pins the packages whose versions affect the printed results:

| Package | Version |
|---|---|
| qiskit | 2.6.1 |
| qiskit-aer | 0.18.0 |
| qiskit-ibm-runtime | 0.51.0 |
| numpy | 2.5.3 |
| scipy | 1.18.1 |

It also installs Matplotlib, pylatexenc, scikit-learn, pytest and JupyterLab, unpinned.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Check the installation:

```python
import qiskit, qiskit_aer, qiskit_ibm_runtime
print(qiskit.__version__, qiskit_aer.__version__,
      qiskit_ibm_runtime.__version__)
```

You should see `2.6.1 0.18.0 0.51.0`. Newer versions usually work, but outputs may differ slightly and deprecated features may print warnings.

## 3. Run the companion code

Run one script:

```bash
python code/ch07/bell-four.py
```

Run every script of a chapter, capturing its output, with the helper used to build the book:

```bash
python tools/run_code.py ch07
python tools/run_code.py ch05 ch06     # several chapters
python tools/run_code.py               # the whole book
```

The helper writes each script's output to the `.txt` file beside it, replacing the output saved from the book's own run. To compare your results with the book's, run `git diff code/`; to restore the book's outputs, run `git checkout -- code/`.

Figures produced by the scripts are written to `figures/chNN/`. These folders must exist before a plotting script runs; each one holds an empty `.gitkeep` file so that Git keeps it.

Every script can also be pasted into a notebook cell (start JupyterLab with `jupyter lab`).

## 4. Scripts that need an IBM Quantum account

Hardware access is optional for every exercise in the book. Scripts whose first line is `# norun` submit work to IBM Quantum hardware. They need an IBM Quantum account and use your processor time, so `tools/run_code.py` skips them. There are 11:

```
code/ch04/real.py
code/ch05/ibm-get.py
code/ch05/ibm-key.py
code/ch05/ibm-run.py
code/ch08/dynamic-hardware.py
code/ch15/vqe_hardware.py
code/ch17/runtime_resilience.py
code/ch18/batch_mode.py
code/ch18/job_mode.py
code/ch18/session_mode.py
code/ch18/tfim_hardware.py
```

To run them yourself:

1. Sign up at <https://quantum.cloud.ibm.com> and create an instance on the free Open Plan. At the time of writing, the Open Plan provides up to 10 minutes of quantum processor time in each rolling 28-day window, and instances can be created only in the `us-east` region.
2. Copy your API key and the instance's identifier (its CRN) from the dashboard.
3. Save them once on your computer:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="YOUR_API_KEY",
    instance="YOUR_INSTANCE_CRN",
    set_as_default=True,
)
```

Never paste your API key into a notebook that you share or upload, or commit it to a repository. If a key is exposed, delete it on the platform and create a new one.

## 5. Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `ImportError: cannot import name 'execute'` | You are following an old tutorial. `execute` was removed in Qiskit 1.0. Use the Sampler and Estimator primitives (Chapter 5). |
| `ModuleNotFoundError: qiskit.pulse` | Qiskit Pulse was removed in Qiskit 2.0. |
| Counts look reversed (`"01"` instead of `"10"`) | Qiskit orders bits with qubit 0 on the right (Chapter 7). |
| `qc.draw("mpl")` fails | Install `matplotlib` and `pylatexenc`. |
| `FileNotFoundError: 'figures/chNN/...'` | Run the script from this top-level folder, not from inside `code/`. |
| Results differ from the book | Different package versions or missing seeds. Check versions and pass `seed=` or `seed_simulator=`. |
| Estimator complains about the observable size | Map the observable to the transpiled layout with `obs.apply_layout(isa.layout)` (Chapter 8). |
| Deprecation warning for `SamplerV2` from `qiskit_ibm_runtime` | Use the client-side primitives in `qiskit_ibm_runtime.executor_sampler` and `executor_estimator` (Chapters 5 and 18). |
| A job waits in the queue for a long time | Public devices are shared. Use a noisy simulator while developing, and submit only final experiments. |

## Corrections

If you find a mistake in the book or the code, please open an issue on this repository or write to the address given in the book's Preface. Corrections will be listed here.
