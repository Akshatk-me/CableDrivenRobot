# ADR-0006: Reduce oscillation with motion planning before feedback control

- **Status:** accepted
- **Date:** 2026-10-05
- **Related:** R-08, Q-C1–Q-C3, Q-D1, Q-D2

## Context

A suspended 4-cable platform swings after moves (ADR-0001). We need settling within R-08. "Control" can
mean shaping the commanded motion (no sensors) or measuring the platform and correcting it (feedback).

## Options considered

| Option                                                                                             | Pros                                                                                 | Cons                                                                 |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| A. Motion planning only: S-curve profiles and input shaping tuned to the predicted swing frequency | No sensors; works with open-loop steppers; well-proven (cranes, 3D-printer firmware) | Depends on knowing the swing frequency; doesn't correct disturbances |
| B. Feedback from an IMU or camera on the platform                                                  | Corrects disturbances and model errors                                               | Needs sensors, estimation and tuning; large time cost                |
| C. Both                                                                                            | Best performance                                                                     | Most work                                                            |

## Decision

Option A. Feedback control is deferred (see roadmap).

## Consequences

- The simulation must predict the swing frequencies (Q-C1) and how they vary across the workspace.
- Q-D2 checks whether one input shaper works over the whole workspace or needs to vary with position.
- An IMU may still be added to _measure_ swing for validation, without closing the loop.
- Wrong if: measured settling misses R-08 even with the best profile from Q-D1.
