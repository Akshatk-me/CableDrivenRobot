# Requirements (v1)

**Status:** frozen for presentation 2. Changes go through an ADR and bump the version.

## Problem statement

Build a cable-driven parallel robot that automatically picks small rigid objects from known positions and
places them at other known positions, within a budget of ₹5,000 plus components available in the lab.

## Objectives

1. Demonstrate repeatable, automatic pick-and-place with a 4-cable suspended CDPR.
2. Characterise the robot's workspace, accuracy, speed and oscillation through simulation **and** experiment,
   and show the two agree.
3. Reduce platform oscillation using motion planning (trajectory shaping), without feedback sensors.

## Scope

**In scope:** 3-axis position control (x, y, z) of the platform; pre-programmed pick and place coordinates;
an electromagnet gripper; open-loop stepper control.

**Out of scope (v1):** controlling platform orientation; vision; feedback control from platform sensors;
grasping arbitrary objects.

## Requirements

"Target" must be met at the final demo. "Stretch" is attempted only after all targets are met.

| ID   | Requirement                            | Target                                                            | Stretch            | Verification                                                                  |
| ---- | -------------------------------------- | ----------------------------------------------------------------- | ------------------ | ----------------------------------------------------------------------------- |
| R-01 | Frame size                             | 640 × 640 × 600 mm (12 × 600 mm 2020 bars)                        | —                  | Measure                                                                       |
| R-02 | Usable workspace, all cables taut      | 350 × 350 mm footprint, 200 mm vertical travel                    | 450 × 450 × 300 mm | Command workspace corners; check every cable stays taut. Predicted by `Q-A1`. |
| R-03 | Payload (object only)                  | 100 g                                                             | 250 g              | Calibrated weights                                                            |
| R-04 | Objects                                | 40 mm rigid blocks with a steel washer on top, at known positions | Mixed sizes        | 3D-printed test set                                                           |
| R-05 | Position accuracy                      | ±5 mm                                                             | ±2 mm              | Command a point, measure landing on graph paper (`EXP-03`)                    |
| R-06 | Repeatability                          | ±2 mm                                                             | ±1 mm              | Return to one point 10×, measure spread                                       |
| R-07 | Max platform speed                     | 100 mm/s                                                          | 250 mm/s           | Time a known distance                                                         |
| R-08 | Settling time after a move             | Swing below ±3 mm within 1.5 s                                    | 0.5 s              | Slow-motion video against a ruler. Predicted by `Q-C2`.                       |
| R-09 | Pick-and-place cycle                   | ≤ 15 s for a 300 mm move                                          | ≤ 8 s              | Stopwatch, mean of 10 cycles                                                  |
| R-10 | Success rate                           | 9 of 10                                                           | 19 of 20           | Count                                                                         |
| R-11 | Platform tilt / twist during operation | Tilt ≤ 5°, twist ≤ 15°                                            | —                  | Phone level app; predicted by `Q-A3`                                          |
| R-12 | No lost steps in normal operation      | Required torque ≤ 70% of available torque at all times            | —                  | Predicted by `Q-B3`; checked by returning home after 20 cycles                |
| R-13 | Safety                                 | Emergency stop cuts motor power; cables never whip if one snaps   | —                  | Inspection, E-stop test                                                       |
| R-14 | Budget                                 | ≤ ₹5,000 purchased, all with GST bills                            | —                  | `hardware/bom.md` total                                                       |

## Constraints

- Controller: TIVA (TM4C123) by default; any other board needs the professor's prior approval.
- Motors: NEMA 17 from the lab (model and torque to be confirmed — see `sim/params.yaml`).
- All purchases need a GST bill with the professor's name and department address, plus proof of payment.

## Changelog

| Version | Date       | Change             |
| ------- | ---------- | ------------------ |
| v1      | 2026-10-05 | Initial frozen set |
