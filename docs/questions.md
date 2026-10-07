# Open engineering questions

Each question has an ID, the decision it informs, how we plan to answer it, and a status.
When a question is answered, fill in **Answer** with a one-line result and a link to the simulation
notebook or experiment that produced it. Don't delete answered questions; they are the project's history.

Status: `open` · `in progress` · `answered` · `dropped` (with reason)

## A. Statics — where can the robot hold the platform?

These underpin everything else.

| ID | Question | Informs | Method | Status | Answer |
|---|---|---|---|---|---|
| Q-A1 | Where can the platform be held with all 4 cables above minimum tension? | R-01 workspace | Statics sim, grid over workspace | in progress | Point-mass result ([01](../sim/notebooks/01_statics_workspace.py)): the binding limit is the *slackest* cable, not motor torque. With 0.28 kg moving mass and T_min = 0.5 N, pulleys at 570 mm cover only 41–53% of the R-01 area; at 300 mm, 97–100%. All heights cover 100% at T_min = 0.2 N. Needs: 6-DOF check (L3), and a justified T_min (D-11). |
| Q-A2 | What are the cable tensions and holding motor torques at each point? | Spool radius, torque margin | Statics sim | in progress | Max static tension in the work area is 2–3.3 N, vs 28 N available (10 mm spool, 0.4 N·m, 70% margin). Holding torque is not a constraint; dynamics (Q-B3) may still be. |
| Q-A3 | How much does the platform tilt when it hangs at points away from the centre? | D-09, attachment rectangle size | 6-DOF statics (equilibrium orientation) | open | |

## B. Moving — what happens during a move?

| ID | Question | Informs | Method | Status | Answer |
|---|---|---|---|---|---|
| Q-B1 | How do the tensions change while accelerating and braking? | — | Inverse dynamics on a planned trajectory | open | |
| Q-B2 | What is the largest acceleration that keeps every cable taut? | D-06, R-06, trajectory limits | Inverse dynamics, sweep acceleration | open | |
| Q-B3 | Does the required motor torque stay below the available torque at the speed it's spinning? | D-10, spool radius | Compare required torque against motor torque–speed curve | open | |

## C. Oscillation — does it swing, and how much?

| ID | Question | Informs | Method | Status | Answer |
|---|---|---|---|---|---|
| Q-C1 | What are the platform's natural frequencies (swing, bounce, twist), and how do they vary across the workspace and payload? | Motion planning design | Linearise the 6-DOF model about equilibrium; eigenvalues | open | |
| Q-C2 | How much overshoot and how long to settle after a typical move? | D-07 | Forward dynamics simulation | open | |
| Q-C3 | Which oscillation dominates — swinging (from the 2 unconstrained motions) or bouncing (from cable stretch)? | What to cancel | Compare mode frequencies and amplitudes | open | Hypothesis: swinging |

## D. Motion planning — can we move fast without swinging?

| ID | Question | Informs | Method | Status | Answer |
|---|---|---|---|---|---|
| Q-D1 | How do trapezoidal, S-curve and input-shaped velocity profiles compare in residual swing vs move time? | Firmware trajectory generator | Forward dynamics, same move with each profile | open | |
| Q-D2 | How sensitive is input shaping to an error in the estimated frequency? | Whether one shaper works everywhere | Sweep frequency error ±30% | open | |

## E. Design sweeps — how do design choices change A–D?

| ID | Question | Informs | Method | Status | Answer |
|---|---|---|---|---|---|
| Q-E1 | How does pulley height change workspace, tensions, swing frequency and settling? | D-02 pulley height (ADR-0008) | Re-run A–C at several heights | open | Hypothesis: taller → lower tension, slower swing |
| Q-E2 | How does the platform attachment rectangle size change tilt and twist stiffness? | Platform design | Re-run A3, C1 | open | |
| Q-E3 | How far below the attachment plane should the payload hang? | Gripper mount | Re-run A3, C1 | open | |
| Q-E4 | What spool radius best trades torque margin against speed? | Spool design | Re-run B3 at several radii | open | |
| Q-E5 | Would ballast mass on the platform enlarge the taut region enough to justify the extra inertia? | D-11, platform mass | Statics: slack margin scales linearly with weight; then check Q-B3 | in progress | Statics ([02](../sim/notebooks/02_statics_sensitivity.py)): margin is exactly proportional to mass, so mass needed = T_min / (worst margin per kg). The empty return trip (0.18 kg) is the binding case. Ballast needed: at 300 mm pulleys, 0 kg for T_min ≤ 0.3 N, 0.11 kg for 0.5 N; at 550 mm, 0.03 / 0.13 / 0.34 kg for 0.2 / 0.3 / 0.5 N. Cost of mass still to check in dynamics (Q-B3). |
| Q-E6 | What minimum cable tension do we actually need (sag, staying on pulleys, braid stiffness at low load)? | D-11 | Sag calculation + EXP-01 at low loads | open | |

## F. Model trust — can we believe the simulation?

| ID | Question | Informs | Method | Status | Answer |
|---|---|---|---|---|---|
| Q-F1 | What is the cable's axial stiffness EA? | `params.yaml` | `EXP-01` cable stretch test | open | |
| Q-F2 | What is the damping of the real system? | `params.yaml` | `EXP-04` settling video, fit decay | open | |
| Q-F3 | Does the forward-dynamics model predict the measured settling within 25%? | Trust in C and D results | Compare `EXP-04` with sim | open | |
| Q-F4 | Is the simulation converged in time step? | Trust | Halve max step; results change < 1% | open | |
