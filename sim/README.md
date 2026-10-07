# Simulation

See [docs/simulation-plan.md](../docs/simulation-plan.md) for the model layers, assumptions and validation plan.

## Layout (planned)

```
sim/
  params.yaml          All physical parameters, with sources. Edit numbers here, never in code.
  cdpr/                Model code, built up layer by layer
    params.py          Loads params.yaml
    kinematics.py      L0: cable lengths from platform pose
    statics.py         L1, L3: tension distribution, workspace, equilibrium orientation
    dynamics.py        L2, L4: inverse and forward dynamics
    trajectory.py      Velocity profiles: trapezoid, S-curve, input-shaped
  notebooks/           One notebook per question group; each states the question IDs it answers
  tests/               Sanity checks with known answers (symmetry, hand calculations)
```

## Setup (uv)

Dependencies are declared in `pyproject.toml` at the repo root and pinned in `uv.lock`.

```bash
uv sync                                              # create .venv and install exact locked versions
uv run pytest                                        # sanity tests — run before trusting any result
uv run python sim/notebooks/01_statics_workspace.py  # writes plots to sim/results/
```

Add a dependency with `uv add <package>`; never edit the lock file by hand.
Plots in `sim/results/` are generated, so they're git-ignored: re-run the script to get them.
The `# %%` markers in each notebook script make it runnable cell-by-cell in VS Code or Jupyter.
