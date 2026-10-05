# ADR-0007: Electromagnet gripper

- **Status:** proposed
- **Date:** 2026-10-05
- **Related:** R-03, R-04, R-07

## Context

The gripper decides which objects can be handled, adds mass to the platform, and is a major factor in
pick success rate. The platform's twist is not controlled (ADR-0001), so the gripper should not need a
particular orientation.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| A. 12 V electromagnet; steel washer glued to each object | Cheap; one digital output; insensitive to twist and small position errors | Objects must carry steel; residual magnetism may delay release |
| B. Small servo claw | Handles plain objects | Heavier; sensitive to orientation and position error |
| C. Suction cup with pump | Handles flat objects | Pump cost and weight; tubing to a moving platform |

## Decision

Proposed: Option A. To be accepted once a magnet is bought and its holding force is checked.

## Consequences

- Test objects (R-04) carry a steel washer on top.
- Needs a MOSFET or relay and a flyback diode.
- Release timing must be measured; a brief reverse pulse may be needed if residual magnetism holds the object.
- The magnet's mass is part of the moving mass in `sim/params.yaml`.
