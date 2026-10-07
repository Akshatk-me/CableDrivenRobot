"""L1 — Statics: the platform held still, treated as a point mass.

Question it answers (Q-A1, Q-A2): at a given position, what tension does each cable carry,
and is there a way to hold the platform there with every cable taut?

Physics
-------
At rest, the cable pulls and gravity balance:

    T1*u1 + T2*u2 + T3*u3 + T4*u4 = W,     W = (0, 0, m*g)

Stack the directions as columns of a 3x4 matrix U, and the tensions as a vector T:

    U @ T = W                       3 equations, 4 unknowns

So there are infinitely many solutions. They all have the form

    T = T0 + lam * n

  T0  = pinv(U) @ W   the smallest-norm solution (least total "effort")
  n   = null vector of U: a set of tensions with U @ n = 0. Adding it changes the tensions
        without moving the platform, like two people pulling a rope from both ends harder.
        For a symmetric frame it looks like (+, -, +, -): tighten one diagonal pair, slacken the other.
  lam = a free number we get to choose.

Each cable must stay above min_tension:  T0_i + lam*n_i >= T_min  →  a lower or upper limit on lam.
If all four limits leave a non-empty interval [lam_lo, lam_hi], the point is holdable ("feasible").
We then pick the lam closest to 0 inside that interval (the smallest tensions that keep everyone taut).

Limitations (labelled, per ADR-0002)
------------------------------------
- Point mass: forces are balanced, moments are NOT. Cable directions use the real corner
  attachments on a level platform, but whether the platform would actually stay level is
  the 6-DOF question Q-A3 (layer L3).
- Motor torque check here is at standstill only. Speed-dependent limits come with dynamics (L2).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .kinematics import cable_directions
from .params import Params


@dataclass
class StaticsResult:
    feasible: bool          # all cables >= min_tension AND all <= max_tension
    taut_possible: bool     # all cables >= min_tension (ignores motor limit)
    tensions: np.ndarray    # (4,) chosen tensions [N]; NaN if not taut_possible
    lam_interval: tuple     # (lam_lo, lam_hi); lo > hi means no valid tension set


def null_vector(U: np.ndarray) -> np.ndarray:
    """Unit vector n with U @ n = 0, for a full-rank 3x4 matrix U."""
    _, _, Vt = np.linalg.svd(U)
    return Vt[-1]


def solve_tensions(p: np.ndarray, prm: Params) -> StaticsResult:
    """Tension distribution for a point-mass platform held at position p."""
    U = cable_directions(p, prm).T                   # (3, 4): column i is u_i
    W = np.array([0.0, 0.0, prm.moving_mass * prm.g])

    T0 = np.linalg.pinv(U) @ W
    n = null_vector(U)

    # Each cable gives a bound on lam from  T0_i + lam * n_i >= T_min.
    lo, hi = -np.inf, np.inf
    for t0, ni in zip(T0, n):
        if abs(ni) < 1e-12:                         # this cable's tension can't be changed
            if t0 < prm.min_tension:
                lo, hi = np.inf, -np.inf
            continue
        bound = (prm.min_tension - t0) / ni
        if ni > 0:
            lo = max(lo, bound)
        else:
            hi = min(hi, bound)

    if lo > hi:
        return StaticsResult(False, False, np.full(4, np.nan), (lo, hi))

    lam = float(np.clip(0.0, lo, hi))
    T = T0 + lam * n
    feasible = bool(np.all(T <= prm.max_tension))
    return StaticsResult(feasible, True, T, (lo, hi))


def best_slack_margin(p: np.ndarray, prm: Params) -> float:
    """Largest possible tension in the SLACKEST cable at position p [N]. Negative = can't keep all taut.

    This is the tautness margin, and it doesn't depend on which min_tension we pick:
    the point is holdable with min_tension = X exactly when this value is >= X.

    Over all valid tension sets T0 + lam*n, maximise min_i(T_i). Each T_i is a straight line in lam,
    so min_i(T_i) is a tent shape; its peak is where two lines with opposite slopes cross.
    """
    U = cable_directions(p, prm).T
    W = np.array([0.0, 0.0, prm.moving_mass * prm.g])
    T0 = np.linalg.pinv(U) @ W
    n = null_vector(U)
    up, down = np.where(n > 1e-12)[0], np.where(n < -1e-12)[0]
    if len(up) == 0 or len(down) == 0:              # tensions can't be traded off; take lam = 0
        return float(T0.min())
    # Peak of the tent: try every crossing of a rising line with a falling line, keep the best.
    best = -np.inf
    for i in up:
        for k in down:
            lam = (T0[k] - T0[i]) / (n[i] - n[k])
            best = max(best, float(np.min(T0 + lam * n)))
    return best


def worst_margin_per_kg(prm: Params, xs, ys, zs) -> float:
    """Smallest slack margin over a box of positions, per kg of moving mass [N/kg].

    Every tension in the statics problem is proportional to the weight, so the slack margin is
    too. Dividing by mass gives a number that holds for ANY mass:
        margin(m) = m * worst_margin_per_kg
    and the mass needed to keep every cable above T_min everywhere in the box is
        m_needed = T_min / worst_margin_per_kg
    """
    worst = min(best_slack_margin(np.array([x, y, z]), prm) for x in xs for y in ys for z in zs)
    return worst / prm.moving_mass


def tension_map(xs: np.ndarray, ys: np.ndarray, z: float, prm: Params) -> np.ndarray:
    """Max cable tension over a horizontal grid at height z. NaN where the cables can't all stay taut.

    Returns an array of shape (len(ys), len(xs)) — rows are y, columns are x (image convention).
    """
    out = np.full((len(ys), len(xs)), np.nan)
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            r = solve_tensions(np.array([x, y, z]), prm)
            if r.taut_possible:
                out[j, i] = r.tensions.max()
    return out
