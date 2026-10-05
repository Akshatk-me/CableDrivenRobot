# ADR-0005: Model steppers as position sources with a torque check

- **Status:** accepted
- **Date:** 2026-10-05
- **Related:** R-12, Q-B3, assumption S1

## Context

The first idea was to model each stepper as "provides its rated torque". But the rated (holding) torque
applies only at standstill, and the torque a stepper can give falls sharply with speed. More importantly,
a stepper doesn't output a chosen torque: it moves to its commanded angle, using whatever torque that takes,
until the required torque exceeds what it can give — and then it skips steps.

## Options considered

| Option                                                                                             | Pros                                                                                            | Cons                                                     |
| -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| A. Constant torque source at rated torque                                                          | Simple                                                                                          | Physically wrong for a stepper; ignores speed dependence |
| B. Ideal position source; check required torque against the torque–speed curve afterwards          | Matches how steppers behave in normal operation; simple; directly answers "will it skip steps?" | Doesn't simulate what happens _after_ a skip             |
| C. Stepper as a stiff torsional spring toward the commanded angle, τ = −τ_hold·sin(50·(θ − θ_cmd)) | Captures step loss and motor compliance                                                         | More parameters; stiffer equations                       |

## Decision

Option B for M1 and M2. Option C is an upgrade if steps are lost in testing or the model disagrees with experiment.

## Consequences

- Spool angle follows the planned trajectory exactly. Required motor torque = spool radius × cable tension
  - rotor inertia × angular acceleration.
- Each simulation must plot required torque against available torque at the current speed. R-12 requires
  ≤ 70% of available.
- We need the lab motor's torque–speed curve. Until found, use a typical NEMA 17 curve and flag it as assumed.
