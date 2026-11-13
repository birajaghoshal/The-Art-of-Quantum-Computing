# Peek inside a preset pass manager: its six stages
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeFez

pm = generate_preset_pass_manager(optimization_level=2,
                                  backend=FakeFez(),
                                  seed_transpiler=11)
for stage in pm.stages:
    sub = getattr(pm, stage)
    if sub is None:
        print(f"{stage:13s} (empty)")
        continue
    names = []
    for task in sub.to_flow_controller().tasks:
        for p in getattr(task, "tasks", [task]):
            names.append(type(p).__name__)
    print(f"{stage:12s} {len(names):2d} passes, first: {names[0]}")
