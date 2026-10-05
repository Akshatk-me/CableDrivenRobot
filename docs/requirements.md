# Requirements (v2)

Requirements say **what** the robot must do and the limits it must live within, never **how**.
Anything that is a choice we make to satisfy these (frame size, speed, settling time, tilt limits, gripper type)
is a design parameter, derived and tracked in [design-parameters.md](design-parameters.md).

Test for any line here: *could a different, valid design satisfy it?* If the line only makes sense for one
particular design, it belongs in design parameters or an ADR, not here.

## Problem statement

Automatically move small rigid objects from known pick locations to known place locations using a
cable-driven parallel robot, within ₹5,000 plus components available in the lab.

## Objectives

1. Demonstrate repeatable, automatic pick-and-place with a cable-driven parallel robot.
2. Show that simulation predicts the robot's behaviour, by comparing it with experiments.

## Functional and performance requirements

| ID | Requirement | Target | Stretch | Verification |
|---|---|---|---|---|
| R-01 | Work area: region on the work surface where objects can be picked and placed | 350 × 350 mm | 450 × 450 mm | Pick and place at the four corners and centre |
| R-02 | Lift: objects carried clear of the work surface | ≥ 100 mm above the surface | — | Measure during a move |
| R-03 | Payload | 100 g | 250 g | Calibrated weights |
| R-04 | Objects | Rigid, fits within a 50 mm cube | — | Test object set |
| R-05 | Placement accuracy: object centre vs commanded place location | ±5 mm | ±2 mm | Graph paper, 10 placements |
| R-06 | Cycle time: pick, move 300 mm, place | ≤ 15 s | ≤ 8 s | Stopwatch, mean of 10 cycles |
| R-07 | Reliability: successful automatic cycles | 9 of 10 | 19 of 20 | Count |
| R-08 | Safety | Emergency stop removes motor power; a cable failure does not endanger people | — | E-stop test, inspection |

## Constraints

Fixed by the course, not chosen by us.

| ID | Constraint |
|---|---|
| C-01 | Purchases ≤ ₹5,000, each with a GST bill (professor's name, department address) and proof of payment |
| C-02 | Controller: TIVA (TM4C123), or another board with the professor's prior approval |
| C-03 | Actuators: NEMA 17 steppers available in the lab |
| C-04 | Dates: presentation 2 on 8 Oct, presentation 3 on 29 Oct, final demo on 26 Nov 2026 |

## Out of scope (v2)

Controlling platform orientation, vision, arbitrary object shapes.

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2026-10-05 | Initial set |
| v2 | 2026-10-05 | Stripped to needs and constraints. Frame size, speed, settling, repeatability, tilt and torque margin moved to design parameters. Work area redefined as the area on the work surface, not a 3D volume. |
