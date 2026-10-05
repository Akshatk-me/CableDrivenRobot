# ADR-0001: Suspended 4-cable configuration with motors at the bottom

- **Status:** accepted
- **Date:** 2026-10-05
- **Related:** R-01, D-09, Q-A1, Q-C3

## Context

The platform must be positioned in 3D with the motors available in the lab (NEMA 17) and a small budget.
Cables can only pull, so every direction the platform must be held in needs a cable, or gravity, opposing it.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| A. Suspended: 4 cables from top-corner pulleys, gravity pulls down | Few motors; simple; gravity keeps cables taut | Orientation not fully controlled (4 cables, 6 motions); platform can swing; workspace limited near the top and edges |
| B. Fully constrained: 8 cables, some from below | Controls all 6 motions; stiffer | Twice the motors and drivers; cable interference; much harder to build and control |
| C. 3 cables to a single point | Fewest motors | Very small, triangular workspace; little resistance to swing |

## Decision

Option A. Motors sit at the bottom corners; each cable runs up the corner upright, over a pulley at the
top corner, and down to the platform.

## Consequences

- Only position (x, y, z) is commanded. Tilt and twist settle wherever forces balance (D-09 sets limits).
- Two motions are unconstrained by cable lengths and held only by gravity → expect pendulum-like swinging
  (Q-C3). Motion planning must handle it (ADR-0006).
- Motors low down keep the centre of mass low and wiring short.
- What matters geometrically is the cable exit point at each top pulley, not the motor position.
- Wrong if: swing cannot be brought within D-07 by motion planning.
