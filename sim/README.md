# Simulation

See [docs/simulation-plan.md](../docs/simulation-plan.md) for the model layers, assumptions and validation plan.

## Layout (planned)

```
sim/
  params.yaml          All physical parameters, with sources. Edit numbers here, never in code.
  requirements.txt     Python dependencies
  cdpr/                Model code, built up layer by layer
    params.py          Loads params.yaml
    kinematics.py      L0: cable lengths from platform pose
    statics.py         L1, L3: tension distribution, workspace, equilibrium orientation
    dynamics.py        L2, L4: inverse and forward dynamics
    trajectory.py      Velocity profiles: trapezoid, S-curve, input-shaped
  notebooks/           One notebook per question group; each states the question IDs it answers
  tests/               Sanity checks with known answers (symmetry, hand calculations)
```

## Setup

```bash
pip install -r requirements.txt
```

Or open a notebook in Google Colab and run `!pip install -r requirements.txt` in the first cell.
