# ADR-0004: Python (numpy/scipy) for simulation

- **Status:** accepted
- **Date:** 2026-10-05
- **Related:** docs/simulation-plan.md

## Context

The professor wants dynamic simulations. The team has limited time, wants to understand the physics,
and needs results that can be checked against experiments and put on slides.

## Options considered

| Option                                                              | Pros                                                                                                   | Cons                                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| A. Python: numpy, scipy (`solve_ivp`), matplotlib, in Jupyter/Colab | Free; equations written by hand, so the physics is visible and explainable; fast to change; easy plots | Basic visuals; we write the model ourselves                                  |
| B. MATLAB / Simulink / Simscape Multibody                           | Polished; may be expected in some courses                                                              | Cables don't fit the standard blocks well; time spent learning the tool      |
| C. Physics engine (MuJoCo, PyBullet, Gazebo)                        | Good 3D visuals                                                                                        | Hides the equations; cable/tendon setup is fiddly; harder to explain results |
| D. CAD motion study                                                 | Uses the CAD model                                                                                     | Cannot model one-way, stretchy cables                                        |

## Decision

Option A. Model code lives in `sim/`, parameters in `sim/params.yaml`, analyses in `sim/notebooks/`.

## Consequences

- We must write the equations ourselves, which is the learning goal and makes results defensible.
- We must check numerical issues ourselves (time-step convergence, stiff cables) — see the checklist in
  the simulation plan.
- If 3D visuals are needed for the final demo, MuJoCo can be added later as a visualiser without
  replacing the model.
- Wrong if: the professor requires MATLAB, in which case the equations port directly.
