# CDPR Pick-and-Place

A low-cost **cable-driven parallel robot (CDPR)** for automated pick-and-place, built as a course project.
Four NEMA 17 steppers at the bottom corners of a 2020 aluminium cube reel cables up over pulleys at the
top corners and down to the corners of a platform, which carries a gripper.

> This repo is also a deliberate exercise in **designing a complete system well**: requirements first,
> questions written down before answers, decisions recorded with their reasoning, and every claim backed
> by a simulation or an experiment.

## Status

| Item | State |
|---|---|
| Requirements | v2 — see [docs/requirements.md](docs/requirements.md); design choices in [docs/design-parameters.md](docs/design-parameters.md) |
| Mechanical | Frame and parts being procured |
| Simulation | Planned — see [docs/simulation-plan.md](docs/simulation-plan.md) |
| Firmware | Not started; controller board pending approval |

## Key dates

| Date | Milestone |
|---|---|
| Thu 8 Oct 2026 | Presentation 2 — mechanical build mostly done, first simulations |
| Thu 29 Oct 2026 | Presentation 3 |
| Thu 26 Nov 2026 | Final demo and presentation |

Details in [docs/roadmap.md](docs/roadmap.md).

## How this repo is organised

```
README.md                 You are here
docs/
  requirements.md         What the robot must do, and how each requirement is tested
  design-parameters.md    Choices derived from the requirements, each traced to the question that decides it
  questions.md            Open engineering questions — the things we need to find out
  roadmap.md              Milestones, what is due when, and what is deliberately deferred
  architecture.md         The system broken into subsystems, and the interfaces between them
  simulation-plan.md      Model layers, assumptions, and how each model is validated
  adr/                    Architecture Decision Records: one file per design decision
  experiments/            One file per physical test: hypothesis, method, result, conclusion
hardware/
  bom.md                  Bill of materials: part, spec, source, status, cost, bill
sim/
  params.yaml             Single source of truth for every physical parameter used in simulation
  README.md               How to run the simulations
```

## Working rules

These are the habits this project is practising:

1. **Requirements are testable.** Every requirement has a number and a way to verify it.
2. **Questions before answers.** Anything we don't know goes into `questions.md` with an ID (e.g. `Q-B2`).
   When it's answered, the answer links to the simulation or experiment that settled it.
3. **Decisions are recorded.** Any choice that would be expensive to reverse gets an ADR in `docs/adr/`,
   including the options we rejected and why. ADRs are never edited after acceptance; a changed decision
   gets a new ADR that supersedes the old one.
4. **One source of truth for numbers.** Physical parameters live in `sim/params.yaml`, each with its
   source (datasheet, measured, or assumed). Assumed values are flagged until measured.
5. **Simulations answer questions.** Each simulation states which question it answers. A plot that
   answers nothing doesn't go in the presentation.
6. **Simulations are checked against reality.** Each model layer has a validation experiment.
