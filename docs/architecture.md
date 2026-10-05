# System architecture

The robot is split into subsystems with clear interfaces, so each can be designed, built and tested on
its own. When something goes wrong, the interface tells you which side to look at.

## Subsystems

```
                 ┌────────────────────┐
  Pick/place     │  1. Task layer     │  List of (pick, place) coordinates
  coordinates ──▶│     (firmware)     │
                 └─────────┬──────────┘
                           │ target (x, y, z), gripper on/off
                 ┌─────────▼──────────┐
                 │ 2. Motion planner  │  Velocity profile: trapezoid / S-curve / input-shaped
                 │     (firmware)     │
                 └─────────┬──────────┘
                           │ platform position p(t) at each control tick
                 ┌─────────▼──────────┐
                 │ 3. Inverse         │  Cable lengths L_i(t) = |A_i − (p + R·b_i)|
                 │    kinematics      │
                 └─────────┬──────────┘
                           │ motor step counts n_i(t)
                 ┌─────────▼──────────┐
                 │ 4. Drivers + motors│  4 × NEMA 17, step/dir drivers
                 └─────────┬──────────┘
                           │ spool rotation → cable length
                 ┌─────────▼──────────┐
                 │ 5. Mechanical plant│  Frame, pulleys, cables, platform, payload
                 └─────────┬──────────┘
                           │
                 ┌─────────▼──────────┐
                 │ 6. Gripper         │  Electromagnet + MOSFET
                 └────────────────────┘
```

## Interfaces

| From → To | Interface | Contract |
|---|---|---|
| Task → Planner | Target point, gripper command | Targets must lie inside the verified workspace (`Q-A1`) |
| Planner → IK | Platform position p(t) sampled at the control rate | Respects max velocity and acceleration from `Q-B2` |
| IK → Drivers | Step counts per motor | Steps per mm from `EXP-02`; never exceeds max step rate |
| Motors → Plant | Spool torque and angle | Required torque ≤ 70% of available torque (D-10) |
| Firmware → Gripper | Digital pin | On/off; release delay to be measured |

## Coordinate frame

- Origin: centre of the floor of the frame.
- x, y: horizontal, along the frame edges. z: up.
- `A_i`: cable exit point on pulley i (top corner). `b_i`: cable attachment point on the platform,
  in the platform's own frame. `R`: platform rotation.
- Cables are numbered 1–4 counter-clockwise from the (−x, −y) corner, viewed from above.

All code, drawings and documents use this convention.

## Where the simulation fits

The simulation replaces blocks 4–5 (and later 6) with a model, and reuses blocks 2–3 unchanged. That
means the trajectory and inverse-kinematics code tested in simulation is the same logic that goes on
the controller.
