# ADR-0003: 2020 aluminium cube frame from 12 × 600 mm bars

- **Status:** superseded by ADR-0008
- **Date:** 2026-10-05
- **Related:** D-01, C-01, Q-E1

## Context

The frame carries the pulleys and motors and must stay stiff under cable tension. It needs to be built in
about one day, from parts available in Mumbai, within budget.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| A. 2020 extrusion, L-brackets, drop-in T-nuts | Stiff; adjustable; easy to mount parts anywhere; reusable | Biggest single cost item |
| B. Wood | Cheap; easy to cut | Less stiff and less precise; harder to adjust |
| C. 3D-printed joints with rods or pipes | Cheap | Slow to print; joints flex |

## Decision

Option A. All 12 bars cut to 600 mm. Uprights are full height; horizontals butt against the uprights'
side faces with metal L-brackets on the inside corners. Outer size is 640 × 640 × 600 mm (W × D × H).
Use drop-in (roll-in) T-nuts so parts can be added after assembly.

## Consequences

- One cut length simplifies ordering. Horizontal span between upright faces is 600 mm.
- Height is fixed at 600 mm for now. Q-E1 may recommend a different height; changing it means new
  uprights only, recorded in a new ADR.
- Frame squareness must be checked (equal diagonals) before final tightening, since it sets pulley positions.
- Wrong if: frame visibly flexes under cable tension (assumption S5 in the simulation plan).
