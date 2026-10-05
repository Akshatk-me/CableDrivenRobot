# Simulation plan

## Approach

Build the model in layers. Each layer adds one piece of physics, answers specific questions, and is
checked before the next layer is built on it. Tools: Python with numpy, scipy and matplotlib, run in
Jupyter or Google Colab (see ADR-0004).

## Model layers

| Layer                     | Physics included                                                        | Answers                    | Validated by                                       | Milestone |
| ------------------------- | ----------------------------------------------------------------------- | -------------------------- | -------------------------------------------------- | --------- |
| L0 Kinematics             | Geometry only: cable length from platform pose                          | Cable lengths along a path | Hand calculation at the centre and one corner      | M1        |
| L1 Statics                | Force balance, platform held still, point mass                          | Q-A1, Q-A2                 | Tensions sum to the weight at the centre; symmetry | M1        |
| L2 Inverse dynamics       | Newton's 2nd law along a planned trajectory, point mass, rigid cables   | Q-B1–Q-B3                  | Zero acceleration reduces to L1                    | M1        |
| L3 6-DOF statics          | Rigid platform, corner attachments, equilibrium orientation             | Q-A3                       | Level at the centre (by symmetry)                  | M2        |
| L4 6-DOF forward dynamics | Rigid platform, elastic damped cables, motors as ideal position sources | Q-C1–Q-C3, Q-D1–Q-D2       | EXP-04 settling video (Q-F3)                       | M2        |
| L5 Design sweeps          | L1–L4 run over parameter ranges                                         | Q-E1–Q-E4                  | Trends consistent across layers                    | M2–M3     |

## Modelling choices and assumptions

Every assumption is listed so it can be challenged. If simulation and experiment disagree, check these first.

| #   | Assumption                                                                                               | Why it's reasonable                                                   | Revisit if                             |
| --- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------- |
| S1  | Motors follow their commanded angle exactly; torque is checked against the torque–speed curve afterwards | Steppers are position devices until they run out of torque (ADR-0005) | Steps are lost in testing              |
| S2  | Cables are massless, straight springs that can only pull: T = max(0, k·stretch + c·stretch rate)         | Light braid under tension; sag negligible                             | Long slack cables near workspace edges |
| S3  | Cable stiffness k = EA / L, with EA from EXP-01                                                          | Standard axial stiffness model                                        | Stretch test is non-linear             |
| S4  | Cable exit point is a fixed point at each pulley                                                         | Pulley radius small relative to frame                                 | Errors of a few mm matter              |
| S5  | Frame is rigid                                                                                           | 2020 frame much stiffer than cables                                   | Frame visibly flexes                   |
| S6  | Damping is a single coefficient per cable, tuned to match EXP-04                                         | Simple, and fitted to reality                                         | Decay isn't exponential                |
| S7  | Spool radius is constant                                                                                 | Single layer of thin line on the spool                                | Cable winds over itself                |

## Good-practice checklist for every simulation

- [ ] States which question ID it answers.
- [ ] Reads all physical values from `sim/params.yaml`; no numbers buried in code.
- [ ] Has a sanity check with a known answer (symmetry, hand calculation, limit case).
- [ ] Time step convergence checked (halve max step, result changes < 1%) — Q-F4.
- [ ] Every cable tension is checked to be ≥ 0; a negative tension means a bug or an infeasible command.
- [ ] Plots have units, labels, and a one-line conclusion written underneath.
- [ ] Result recorded in `docs/questions.md`.
