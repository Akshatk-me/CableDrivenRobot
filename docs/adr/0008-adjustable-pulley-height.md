# ADR-0008: 2020 frame with adjustable pulley height

- **Status:** accepted
- **Date:** 2026-10-05
- **Supersedes:** ADR-0003
- **Related:** R-01, R-02, D-01, D-02, Q-A1, Q-E1

## Context

ADR-0003 fixed the frame at 600 mm tall. Height is not a requirement; it's a design parameter (D-02) that
trades holding tension and stiffness against swing frequency and lift range, and Q-E1 is supposed to decide it.
A lower frame (~300 mm) may well be better. But the frame must be built this week, before that simulation exists.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| A. Fixed 600 mm frame (ADR-0003) | Simple | Commits to a height before analysis |
| B. Wait for Q-E1, then build | Height chosen properly | Build misses presentation 2 |
| C. Build 600 mm uprights; mount the top pulleys on brackets that slide along the uprights' T-slots | Build now; height adjustable from ~300 to ~570 mm in minutes; lets us test heights physically too | Pulley mounts need a clamp design; small risk of slipping under tension |

## Decision

Option C. What matters geometrically is the cable exit point at each pulley, not the top of the frame,
so the pulley height *is* the effective frame height. Construction otherwise as in ADR-0003: 2020 extrusion,
metal L-brackets, drop-in T-nuts.

## Consequences

- No commitment to a height until Q-E1 is answered; the simulation sweeps pulley height directly.
- Once decided, a new ADR records the chosen height. Uprights may then be shortened, or left as they are.
- Pulley mounts must clamp with two T-nuts each so they don't slide under cable tension.
- Experiments at two heights become possible, which strengthens the model validation (Q-F3).
