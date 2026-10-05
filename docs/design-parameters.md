# Design parameters

Choices we make to satisfy the [requirements](requirements.md). Each one traces to the requirement it
serves and the question or experiment that will settle it. Values marked **provisional** are working
assumptions, not commitments; they change freely until the deciding analysis is done, then they get an ADR.

| ID | Parameter | Serves | Decided by | Current value | Status |
|---|---|---|---|---|---|
| D-01 | Frame width and depth | R-01 | Q-A1, Q-E1 | 640 × 640 mm (12 × 600 mm bars) | provisional |
| D-02 | Pulley height above the work surface (sets effective frame height) | R-01, R-02, R-06 | Q-A1, Q-E1 | Adjustable, range to test ~300–570 mm (ADR-0008) | open |
| D-03 | Platform attachment rectangle | R-05 | Q-A3, Q-E2 | 100 × 100 mm | provisional |
| D-04 | Payload drop below attachment plane | R-05 | Q-A3, Q-E3 | 30 mm | provisional |
| D-05 | Spool radius | R-03, R-06 | Q-B3, Q-E4 | 10 mm | provisional |
| D-06 | Max platform speed and acceleration | R-06 | Q-B2, Q-B3 | — | open |
| D-07 | Settling time after a move | R-05, R-06 | Q-C2, Q-D1 | — | open |
| D-08 | Repeatability of the platform | R-05 | EXP-03 | — | open |
| D-09 | Allowed tilt and twist of the platform | R-05 | Q-A3 | — | open |
| D-10 | Torque margin: required ≤ fraction of available | R-05, R-07 (no lost steps) | Q-B3 | 70% | provisional |
| D-11 | Minimum cable tension (below = slack) | R-05 | Q-A1 | 0.5 N | provisional |
| D-12 | Gripper type | R-03, R-04, R-07 | ADR-0007 | Electromagnet | proposed |

## Error budget (to fill once D-06 to D-09 are known)

R-05 allows ±5 mm at the object. That total is shared between: platform repeatability (D-08), residual swing
when the gripper releases (D-07), position error from tilt × payload drop (D-09, D-04), and the object
sliding on release. The budget makes the trade-offs explicit, e.g. a longer drop below the platform improves
tilt stability but turns each degree of tilt into more position error.
