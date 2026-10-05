# Architecture Decision Records

An ADR records one design decision: the context, the options considered, what was chosen, and the
consequences. It exists so that in three weeks you (or your professor) can see _why_ something is the way
it is, not just _what_ it is.

## Rules

- One decision per file, numbered in order: `NNNN-short-title.md`.
- Status is one of `proposed`, `accepted`, `superseded by ADR-NNNN`, `rejected`.
- Once accepted, an ADR is not rewritten. If the decision changes, write a new ADR and mark the old one
  as superseded. The trail of changed decisions is valuable.
- Write an ADR when a decision is expensive to reverse, or when someone is likely to ask "why did you do it this way?".

## Index

| ADR                                                 | Title                                                           | Status   |
| --------------------------------------------------- | --------------------------------------------------------------- | -------- |
| [0001](0001-suspended-four-cable-configuration.md)  | Suspended 4-cable configuration with motors at the bottom       | accepted |
| [0002](0002-corner-cable-attachment.md)             | Cables attach to the platform corners                           | accepted |
| [0003](0003-frame-2020-cube.md)                     | 2020 aluminium cube frame from 12 × 600 mm bars                 | accepted |
| [0004](0004-python-for-simulation.md)               | Python (numpy/scipy) for simulation                             | accepted |
| [0005](0005-stepper-modelled-as-position-source.md) | Model steppers as position sources with a torque check          | accepted |
| [0006](0006-motion-planning-before-feedback.md)     | Reduce oscillation with motion planning before feedback control | accepted |
| [0007](0007-electromagnet-gripper.md)               | Electromagnet gripper                                           | proposed |

Template: [0000-template.md](0000-template.md)
