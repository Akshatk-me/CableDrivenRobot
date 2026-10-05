# Experiments

One file per experiment, named `EXP-NN-short-title.md`, using [the template](EXP-00-template.md).
Every experiment states a hypothesis _before_ it's run. Raw data (CSV, photos, video frames) goes in
`docs/experiments/data/EXP-NN/`.

## Planned

| ID     | Title                                        | Answers                     | Milestone | Status  |
| ------ | -------------------------------------------- | --------------------------- | --------- | ------- |
| EXP-01 | Cable stretch test                           | Q-F1 (cable stiffness EA)   | M1        | planned |
| EXP-02 | Spool calibration                            | Steps per mm for each motor | M1        | planned |
| EXP-03 | Positioning accuracy                         | R-05, R-06                  | M2        | planned |
| EXP-04 | Settling after a move (slow-motion video)    | R-08, Q-F2, Q-F3            | M2        | planned |
| EXP-05 | Electromagnet holding force and release time | ADR-0007                    | M2        | planned |

## EXP-01 outline: cable stretch

- **Hypothesis:** PE braid stretches linearly with load, and less than 1% at 10 N.
- **Method:** hang 1.000 m of line from a fixed point; add known weights (0, 0.5, 1, 2 kg); measure length
  each time; repeat unloading.
- **Output:** EA = (force / stretch) × length. Plot force against stretch; the slope gives stiffness.
  Note any hysteresis between loading and unloading.

## EXP-02 outline: spool calibration

- **Hypothesis:** cable reeled in per step = 2π·r / (200 × microsteps), within 2%.
- **Method:** mark the cable; command a fixed number of steps; measure the length reeled in; repeat 5×
  per motor.
- **Output:** measured mm per step for each motor, and its spread.
