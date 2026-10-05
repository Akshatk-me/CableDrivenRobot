# Roadmap

Three milestones, each with a definition of done. A milestone is done when everything in its list is
demonstrably true, not when the work "feels mostly there".

## M1 — Presentation 2 (Thu 8 Oct 2026)

**Theme:** the mechanical plant exists; the first simulations answer the static questions.

| Area | Definition of done |
|---|---|
| Procurement | All parts bought or issued from the lab; BOM complete with GST bills (`hardware/bom.md`) |
| Mechanical | Frame assembled and square; motors, spools and top pulleys mounted; cables strung to a platform |
| Electronics | Drivers wired; each motor can be jogged individually from test code |
| Experiments | `EXP-01` cable stretch, `EXP-02` spool calibration written up |
| Simulation | Kinematics; statics workspace and tension maps (`Q-A1`, `Q-A2`); inverse dynamics on one move (`Q-B1`–`Q-B3`) |
| Decisions | ADRs 0001–0007 accepted or proposed |
| Slides | 7 slides per the professor's format |

**Day plan**

| Day | Work |
|---|---|
| Mon 5 | Check lab inventory; ask professor about controller; print spools and mounts; start simulation |
| Tue 6 | Market run (Lohar Chawl / Nagdevi Street, Lamington Road); assemble frame; mount motors |
| Wed 7 | Pulleys, spools, cables, platform; jog motors; run EXP-01 and EXP-02; slides |
| Thu 8 | Photos; buffer |

## M2 — Presentation 3 (Thu 29 Oct 2026)

**Theme:** the robot moves the platform under coordinated control; simulation predicts oscillation.

| Area | Definition of done |
|---|---|
| Firmware | Inverse kinematics on the controller; coordinated 4-motor moves to commanded (x, y, z); homing |
| Gripper | Electromagnet mounted and switched by the controller |
| Simulation | 6-DOF forward dynamics with elastic cables (`Q-C1`–`Q-C3`); first motion-planning comparison (`Q-D1`) |
| Experiments | `EXP-03` positioning accuracy; `EXP-04` settling video; model compared with experiment (`Q-F3`) |
| Design | Frame height sweep (`Q-E1`) and any resulting ADRs |

## M3 — Final demo (Thu 26 Nov 2026)

**Theme:** reliable pick-and-place meeting the v2 requirements.

| Area | Definition of done |
|---|---|
| Function | Full automatic pick-and-place cycles; R-05 to R-07 measured and reported |
| Motion planning | Best profile from `Q-D1` implemented in firmware; measured improvement in settling |
| Simulation | Validated model; remaining design sweeps (`Q-E2`–`Q-E4`) |
| Report | Requirements table with measured values; all ADRs; answered questions list |

## Deliberately deferred

Writing these down stops them creeping into the schedule.

| Item | Why deferred | Revisit |
|---|---|---|
| Feedback control from platform sensors | Needs sensors we don't have; motion planning should meet D-07 | After M3, if D-07 is missed |
| Orientation control (needs 6+ cables) | Out of v1 scope | Not planned |
| Vision for object detection | Out of v1 scope | Stretch, after M3 targets |
| Cable sag modelling | Cables are light and taut; effect expected to be negligible | Only if sim and experiment disagree |

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Extrusion cutting delayed | M1 mechanical slips | Present parts + partial assembly; order early Tuesday |
| Controller not approved in time | M1 firmware slips | Ask Monday; TIVA is the default fallback |
| Lab NEMA 17 torque unknown | Torque checks unreliable | Read the motor's label; find its datasheet |
| Swing worse than predicted | D-07 missed | Input shaping (`Q-D1`); reduce speed |
| Steps lost under load | R-05/D-10 missed | Larger torque margin: smaller spool radius, lower acceleration |
