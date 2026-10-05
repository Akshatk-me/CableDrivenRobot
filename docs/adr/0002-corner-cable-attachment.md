# ADR-0002: Cables attach to the platform corners

- **Status:** accepted
- **Date:** 2026-10-05
- **Related:** D-09, Q-A3, Q-E2, Q-E3

## Context

The four cables can meet the platform at one central point or at four separated points (its corners).
This choice decides whether the platform resists tilting and twisting, and how complex the model is.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| A. All cables to one central point | No cable torques; point-mass model is exact; simplest | Platform free to twist; swings like a pendulum below the point |
| B. Cables to the four corners | Cables resist tilt and twist; steadier platform | Rigid-body (6-DOF) model needed; small tilt causes small position error |

## Decision

Option B. The payload mass hangs at the centre, below the plane of the attachment points.

## Consequences

- The simulation needs a rigid-body model (L3, L4 in the simulation plan). The point-mass model (L1, L2)
  is used first as an approximation and must be labelled as such.
- Inverse kinematics uses attachment offsets: L_i = |A_i − (p + R·b_i)|.
- Making the attachment rectangle the same shape as the pulley rectangle should keep the platform level
  at the workspace centre (check in Q-A3).
- Hanging the payload below the attachment plane adds gravity's restoring effect on tilt (Q-E3).
- Wrong if: measured tilt or twist exceeds D-09, or the extra model complexity blocks M2.
